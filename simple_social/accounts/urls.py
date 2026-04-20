from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views

app_name = "accounts"

urlpatterns = [
    # ... your other urls
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("signup/", views.SignupUserView.as_view(), name="signup"),
    path("edit/", views.ChangeUserView.as_view(), name="edit_profile"),
]
