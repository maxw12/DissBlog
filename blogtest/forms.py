from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from setuptools._entry_points import _

from .models import Submission, Course, User, Comment

course = Course()


class SubmissionForm(forms.ModelForm):
    """
    Form for submitting a post
    """
    class Meta:
        model = Submission
        fields = ('title', 'tag', 'file', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'please enter name of title here'}),
            'tag': forms.Select(choices=course.name, attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'content': 'Abstract',
        }


class CreateUserForm(UserCreationForm):
    """
    Form to take information to do with django base user model.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].help_text = ""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'date_of_birth', 'password1', 'password2',
                  'type')


class LoginUser(forms.Form):
    """
    Form to log user in
    """
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())


class NewCommentForm(forms.ModelForm):
    """
    Form for adding comment
    """
    class Meta:
        model = Comment
        fields = ("comment_by", "content",)
        widgets = {
            "comment_by": forms.Textarea(attrs={'class': 'form-control'}),
            "content": forms.Textarea(attrs={'required': True, 'class': 'form-control'})
        }


