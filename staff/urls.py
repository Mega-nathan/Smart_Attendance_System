from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path('',views.addStaff,name=" add_Staff "),
    path('staff_login',views.staff_login,name="staff_login"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('staff_logout',views.staff_logout,name="staff_logout"),
    path('add_student',views.add_student,name="add_student")
]