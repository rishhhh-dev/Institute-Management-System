from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    otp = models.IntegerField()


class Course(models.Model):
    name = models.CharField(max_length=50)
    price = models.BigIntegerField()
    duration = models.IntegerField()

    def __str__(self):
        return self.name
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    email =  models.EmailField()
    phone = models.BigIntegerField()
    location =  models.CharField(max_length=100)
    course = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.name