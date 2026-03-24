from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "you@example.com"
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Enter your password"
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Repeat your password"
        })
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']