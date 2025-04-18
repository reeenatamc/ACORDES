from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import FormView

from .models import UserPrompt
from django.contrib.auth import get_user_model
User = get_user_model()

class PromptForm(forms.Form):
    prompt = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Escribe algo...'
    }))
