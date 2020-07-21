from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegistrationForm(UserCreationForm):
	class Meta:
		model = User 
		fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'groups', 'user_permissions']

class ProfileImageForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']


class AccountSettingsForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['phone']

class AccountPrivacyForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email']

