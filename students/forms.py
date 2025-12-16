from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')



# class StudentRegisterForm(forms.ModelForm):
#     class Meta:
#         model = Student
        # fields = ('profile_image', 'bio', 'course', 'year', 'mobile')




class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']


class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['name']


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'description', 'years']



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['bio', 'college', 'course', 'year', 'mobile', 'profile_image']



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['college', 'course', 'year', 'mobile', 'profile_image', 'bio']
