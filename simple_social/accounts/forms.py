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


class CustomUserChangeForm(forms.ModelForm):
    new_password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label="New Password",
        help_text="Leave blank if you don't want to change your password.",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), required=False, label="Confirm New Password"
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email")  # Explicitly define ONLY the fields you want

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data:
            new_password = cleaned_data.get("new_password")
            confirm_password = cleaned_data.get("confirm_password")

            if new_password or confirm_password:
                if new_password != confirm_password:
                    raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user
