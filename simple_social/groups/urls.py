from django.urls import path, include

from groups import apps
from groups.views import GroupCreateView, SingleGroupDetailView, SingleGroupListView

app_name = "groups"
urlpatterns = [
    path("", SingleGroupListView.as_view(), name="group_list"),
    path("new/", GroupCreateView.as_view(), name="group_create"),
    path("<slug:slug>/", SingleGroupDetailView.as_view(), name="single"),
]
