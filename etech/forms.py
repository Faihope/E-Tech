from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_pic','bio']