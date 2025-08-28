from django.db import models
from django.contrib.auth.models import User
from staff.models import Staff

import uuid  # for QR Generation
from .utils import generate_qr_code

from deepface import DeepFace
from django.core.files.base import ContentFile
from io import BytesIO # for storing files in bytes
from PIL import Image




class Student(models.Model):
    name = models.CharField(max_length=100, unique=True)
    face_image = models.ImageField(upload_to="",default='vinoth.jpeg')  # raw image upload
    face_encoding = models.BinaryField(blank=True, null=True)   # store face embedding as bytes
    qr_code = models.BinaryField(blank=True, null=True)         # store QR as image bytes
    qr_token = models.CharField(max_length=255, unique=True, blank=True)  # random id
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Generate QR token if not already
        if not self.qr_token:
            self.qr_token = str(uuid.uuid4())

        # Generate QR code if not already
        if not self.qr_code:
            qr_bytes = generate_qr_code(self.qr_token)
            self.qr_code = qr_bytes

        # Extract face encoding using DeepFace if not already
        if self.face_image and not self.face_encoding:
            try:
                image_path = self.face_image.path
                embedding_obj = DeepFace.represent(img_path=image_path, model_name="Facenet")[0]
                embedding = embedding_obj["embedding"]
                self.face_encoding = np.array(embedding, dtype=np.float32).tobytes()
            except Exception as e:
                print("Face embedding failed:", e)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Session(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_qr = models.BinaryField(blank=True, null=True)
    session_token = models.CharField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.session_token:
            self.session_token = str(uuid.uuid4())
        if not self.session_qr:
            qr_bytes = generate_qr_code(self.session_token)
            self.session_qr = qr_bytes
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} - {self.timestamp}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.name} - {self.session.subject} - {self.status}"
