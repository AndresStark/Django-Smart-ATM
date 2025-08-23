from django.contrib.auth.forms import UserCreationForm, UsernameField

from django import forms

from .models import UserATM, Account

import random

class UserATMCreationForm(UserCreationForm):
    class Meta:
        model = UserATM
        fields = (
            "username",
            "first_name",
            "last_name",
            "phone",
            "address",
            "email",
            "birth_date",
            )
        field_classes = {
            "username": UsernameField,
            "phone": forms.CharField,
            "email": forms.EmailField,
            "birth_date": forms.DateField,
            }

class AccountCreationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = []
    
    password = forms.CharField(max_length=200, label="Contraseña")

    def obtain_password(self):
        return self.cleaned_data['password']