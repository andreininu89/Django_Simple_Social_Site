from django.urls import path
from groups import views  # Standard way to import views

app_name = "groups"

urlpatterns = [
    # 1. The list of all available groups
    path("", views.SingleGroupListView.as_view(), name="group_list"),
    # 2. The page to create a new group
    path("new/", views.GroupCreateView.as_view(), name="group_create"),
    # 3. The detail view (Group Feed) - matches your 'posts/in/<slug>/' pattern
    path("posts/in/<slug:slug>/", views.SingleGroupDetailView.as_view(), name="single"),
    # 4. Join a group
    path("join/<slug:slug>/", views.JoinGroup.as_view(), name="group_join"),
    # 5. Leave a group
    path("leave/<slug:slug>/", views.LeaveGroup.as_view(), name="group_leave"),
]
