from django import forms
from django.contrib.auth.forms import UserCreationForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserSetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

class UserPasswordResetForm(PasswordResetForm):
    pass
