from django.urls import path
from groups import views  # Standard way to import views

app_name = "groups"

urlpatterns = [
    path("", views.SingleGroupListView.as_view(), name="group_list"),
    path("new/", views.GroupCreateView.as_view(), name="group_create"),
    path("posts/in/<slug:slug>/", views.SingleGroupDetailView.as_view(), name="single"),
]
