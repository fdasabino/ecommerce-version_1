from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)

from .models import UserBase


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "id": "login-email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "login-pwd",
            }
        )
    )


class RegistrationForm(forms.ModelForm):

    user_name = forms.EmailField(
        max_length=100,
        help_text="Required",
        error_messages={"required": "Sorry, you will need an email"},
    )
    full_name = forms.CharField(
        label="Full Name", min_length=4, max_length=50, help_text="Required"
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = (
            "full_name",
            "user_name",
        )

    def clean_email(self):
        user_name = self.cleaned_data["user_name"]
        if UserBase.objects.filter(email=user_name).exists():
            raise forms.ValidationError(
                "The email provided is already associated with another user. Please use a different email."
            )
        return user_name

    def clean_full_name(self):
        return self.cleaned_data["full_name"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        return cd["password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Full Name"}
        )
        self.fields["user_name"].widget.attrs.update(
            {
                "class": "form-control mb-3",
                "placeholder": "E-mail",
                "name": "email",
                "id": "id_email",
            }
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Repeat Password"}
        )


class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "id": "form-email",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                "Unfortunately we can not find that email address"
            )
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "New Password",
                "id": "form-newpass",
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "New Password",
                "id": "form-new-pass2",
            }
        ),
    )


class UserEditForm(forms.ModelForm):

    user_name = forms.EmailField(
        label="Account email (can not be changed)",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "email",
                "id": "form-email",
                "readonly": "readonly",
            }
        ),
    )

    full_name = forms.CharField(
        label="Full Name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Full Name",
                "id": "form-fullname",
            }
        ),
    )

    class Meta:
        model = UserBase
        fields = (
            "user_name",
            "full_name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].required = True
        self.fields["user_name"].required = True
