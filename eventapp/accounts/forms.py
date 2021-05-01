from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class CreateUserForm(UserCreationForm):
    class Meta:
        model   = User
        fields  = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(UserChangeForm):

    password = None

    class Meta:
        model   = User
        fields  = ['username', 'first_name', 'last_name', 'email']

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
    
    def clean_email(self):
        if self.is_valid:
            email = self.cleaned_data["email"]
            try:
                profile = Profile.objects.exclude(pk=self.instance.pk).get(email=email)
            except:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % email)

    def clean_username(self):
        if self.is_valid:
            username = self.cleaned_data["username"]
            try:
                profile = Profile.objects.exclude(pk=self.instance.pk).get(
                    username=username
                )
            except:
                return username
            raise forms.ValidationError('Username "%s" is already in use.' % username)

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_pic",
            "website_url",
            "facebook_url",
            "instagram_url",
            "youtube_url",
        ]

        widgets = {
            "website_url": forms.URLInput(attrs={"class": "form-control"}),
            "facebook_url": forms.URLInput(attrs={"class": "form-control"}),
            "instagram_url": forms.URLInput(attrs={"class": "form-control"}),
            "youtube_url": forms.URLInput(attrs={"class": "form-control"}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_pic",
            "website_url",
            "facebook_url",
            "instagram_url",
            "youtube_url",
        ]

        widgets = {
            "website_url": forms.URLInput(attrs={"class": "form-control"}),
            "facebook_url": forms.URLInput(attrs={"class": "form-control"}),
            "instagram_url": forms.URLInput(attrs={"class": "form-control"}),
            "youtube_url": forms.URLInput(attrs={"class": "form-control"}),
        }

