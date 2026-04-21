from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm


# Create your views here.
class SignupUserView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"


class ChangeUserView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("home")
    template_name = "accounts/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        # Keeps the user logged in after password change
        update_session_auth_hash(self.request, self.object)
        messages.success(self.request, "Profile updated successfully!")
        return response


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)
