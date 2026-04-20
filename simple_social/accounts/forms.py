from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )  # Add any custom fields here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = True
        self.fields["email"].required = True
        self.fields["password1"].required = True
        self.fields["password2"].required = True
        self.fields["username"].label = "Display Name: "
        self.fields["email"].label = "Email: "
        self.fields["password1"].label = "Enter Password: "
        self.fields["password2"].label = "Re-enter Password: "


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password",
        )  # Add any custom fields here
