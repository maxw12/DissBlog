from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    This class stores user attribute detail in the User table in the database

    A User instance represents a user that can have certain permissions depending whether
    they're a student, academic or admin
    """
    ADMIN = 1
    STUDENT = 2
    STAFF = 3
    TYPE = (
        (ADMIN, _('Administrator')),
        (STUDENT, _('Student')),
        (STAFF, _('Staff')),
    )
    type = models.PositiveSmallIntegerField(choices=TYPE, default=STUDENT)
    date_of_birth = models.DateField(_('date_of_birth'), default=timezone.now)


class Course(models.Model):
    """
    This class holds information about Course in database table
    """
    name = models.CharField(null=False, max_length=100, default='History')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')


class Submission(models.Model):
    """
    This class holds the details about Submission table in the database, storing
    information including title, course tag, file attached, user, date and likes
    """
    title = models.CharField(max_length=255)
    tag = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True)
    file = models.FileField(upload_to='', blank=True)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_submission')

    def likes_total(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('home')


class Comment(models.Model):
    """
    This class creates holds information about Comment table in the database,
    storing information including Submission model as foreign key, comment content,
    date and user
    """
    post = models.ForeignKey(Submission, related_name="comments", on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ("pub_date",)

    def __str__(self):
        return f"Comment by {self.comment_by}"
