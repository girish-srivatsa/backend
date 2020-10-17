from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.crypto import get_random_string


class Token(models.Model):
    uuid=models.CharField(default='',max_length=40)
    token=models.CharField(max_length=50,default=get_random_string(length=40,allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))


class Course(models.Model):
    name = models.CharField(default="",max_length=100)
    code = models.CharField(default="",max_length=5)

    def __str__(self):
        return self.code+":"+self.name


class Courses(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,blank=True)
    status=models.CharField(default="student",max_length=20)


class UserMy(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_professor=models.BooleanField(default=False)
    tokens=models.ManyToManyField(Token,blank=True)
    courses=models.ManyToManyField(Courses,blank=True)


class Messages(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    message=models.CharField(default="",max_length=200)
    by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="by")
    to=models.CharField(default="student",max_length=20)
    read_by=models.ManyToManyField(User,related_name="read_by",blank=True)
    sent=models.DateTimeField(auto_now=True)
    