from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import UserATM

class UserATMCreationForm(UserCreationForm):
    class Meta:
        model = UserATM
        fields = ("username",)
        field_classes = {"username": UsernameField}