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




# class SkillForm(forms.ModelForm):
#     class Meta:
#         model = Skill
#         fields = ['name']
#         widgets = {
#             'name': forms.TextInput(attrs={'autofocus': True}),
#         }



class SkillForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Skill Name",
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter skill name',
            'autofocus': True
        })
    )

# class InterestForm(forms.ModelForm):
#     class Meta:
#         model = Interest
#         fields = ['name']
#         widgets = {
#             'name': forms.TextInput(attrs={'autofocus': True}),
#         }


class InterestForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Interest Name",
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter interest',
            'autofocus': True
        })
    )



class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'description', 'years']
        widgets = {
            'title': forms.TextInput(attrs={'autofocus': True}),
        }



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
