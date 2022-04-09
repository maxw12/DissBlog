from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# class User(AbstractUser):
#     is_admin = models.BooleanField('is admin', default=False)
#     is_student = models.BooleanField('is student', default=False)
#     is_staff = models.BooleanField('is staff', default=False)
#
#
# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
