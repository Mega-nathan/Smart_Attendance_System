from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path('',views.addStaff,name=" add_Staff "),
    path('staff_login',views.staff_login,name="staff_login"), #login for staff
    path('dashboard',views.dashboard,name="dashboard"), # students attendance statistics
    path('staff_logout',views.staff_logout,name="staff_logout"), # logout for staff
    path('add_student',views.add_student,name="add_student") # add a student 
]