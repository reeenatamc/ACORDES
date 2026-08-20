from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class PromptForm(forms.Form):
    prompt = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Escribe algo..."}))
