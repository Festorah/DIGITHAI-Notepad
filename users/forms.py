from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.utils.translation import gettext_lazy as _
from users.models import AccountUser


class UserLoginForm(forms.Form):
    email_address = forms.EmailField(
        label="Email address",
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "your-email@gmail.com"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your password"}
        ),
    )
    remember_me = forms.BooleanField(
        required=False,
        label="Remember Me",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "placeholder": "Remember Me"}
        ),
    )


class SignUpForm(BaseUserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("First Name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your first name",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("Last Name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your last name",
            }
        ),
    )
    email_address = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "your-email@gmail.com",
                "id": "email_address",
            }
        ),
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
                "id": "password",
            }
        ),
    )
    password2 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Re-enter your password",
                "id": "password",
            }
        ),
    )

    class Meta:
        model = AccountUser
        fields = ("email_address", "password1", "password2")

    def save(self, commit=True):
        email_address = self.cleaned_data["email_address"]
        password = self.cleaned_data["password1"]
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]

        user = AccountUser.objects.create_user(
            email_address=email_address,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        return user
