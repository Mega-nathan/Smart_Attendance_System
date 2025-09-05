import base64
from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from .models import Staff
from student.models import Student
from student.forms import StudentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import face_recognition
from PIL import Image , UnidentifiedImageError
import numpy as np

# Create your views here.


# creating the new staff
def addStaff(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        department = request.POST.get("department")

        # create user for teacher
        user = User.objects.create_user(username=username, password=password)
        user.save()
        print(user)
        print(" User created ")
        # link to staff profile
        staff=Staff.objects.create(user=user, department=department)
        staff.save()

        # return redirect("index")  # go back to home after adding teacher

    return render(request, "index.html")


# staff can login here
def staff_login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(" User logged in succesfully")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('staff_login')

    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# logout your user
def staff_logout(request):
    logout(request)
    return redirect('staff_login')

@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.added_by = request.user  # staff who added
            student.save()

            print(" Student saved Successfully ")
            # Convert QR to base64 for frontend
            
            if student.face_image:
                try:
                    # Open image safely
                    pil_image = Image.open(student.face_image.path)
                    pil_image = pil_image.convert("RGB")  # force RGB
                    image_np = np.array(pil_image)

                    # Generate face encoding
                    encodings = face_recognition.face_encodings(image_np)
                    if encodings:
                        student.face_encoding = np.array(encodings[0]).tobytes()
                        student.save()
                    else:
                        print("No face detected in the image.")
                except UnidentifiedImageError:
                    print("Error: Uploaded file is not a valid image.")
                except Exception as e:
                    print("Error generating face encoding:", e)

            qr_base64 = None
            if student.qr_code:
                qr_base64 = base64.b64encode(student.qr_code).decode('utf-8')

            return render(request, 'student_success.html', {
                'student': student,
                'qr_code': qr_base64
            })
    else:
        form = StudentForm()
    
    return render(request, 'add_student.html', {'form': form})

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})