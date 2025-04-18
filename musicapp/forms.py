from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

# Formulario de Registro
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(max_length=100, label="Email")
    phone = forms.CharField(max_length=100, required=False, label="Phone")
    pfp = forms.ImageField(required=False, label="Profile Picture")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'pfp', 'password1', 'password2']

# Formulario de Login
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
