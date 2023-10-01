from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    ROLES_CHOICES = [
        ('tech', 'Tech_spec'),
        ('manager', 'Manager'),
        ('customer', 'Customer'),
    ]
    role = forms.ChoiceField(choices=ROLES_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
