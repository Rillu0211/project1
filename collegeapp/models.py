from django.db import models


# Create your models here.
# class teachers(models.Model):
#     address=models.CharField(max_length=100,null=True)
#     age=models.IntegerField(null=True)
#     contact_number=models.IntegerField(null=True)
#     image=models.ImageField(upload_to="image/",null=True)

class course(models.Model):
    course_name=models.CharField(max_length=100,null=True)
    fee=models.IntegerField(null=True)

class student(models.Model):
    full_name=models.CharField(max_length=100,null=True)
    address=models.CharField(max_length=100,null=True)
    age=models.IntegerField(null=True)
    joining_date=models.DateField(null=True)
    course=models.ForeignKey(course,on_delete=models.CASCADE,null=True)

from django.contrib.auth.models import User

class teachers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    address = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(upload_to="image/", null=True, blank=True)
    course = models.ForeignKey(course, on_delete=models.SET_NULL, null=True)
