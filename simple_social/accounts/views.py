from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm


# Create your views here.
class SignupUserView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class ChangeUserView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("home")
    template_name = "index.html"

    def get_object(self, queryset=None):
        return self.request.user
