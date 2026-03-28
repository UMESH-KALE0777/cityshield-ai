from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):

        model = CustomUser

        fields = UserCreationForm.Meta.fields + ("email", "phone_number", "city")

        widgets = {

            "username": forms.TextInput(
                attrs={
                    "class":
                    "w-full border p-3 rounded"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class":
                    "w-full border p-3 rounded"
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class":
                    "w-full border p-3 rounded"
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class":
                    "w-full border p-3 rounded"
                }
            ),

        }
