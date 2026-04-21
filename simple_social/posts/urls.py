from django.urls import path
from posts import views

app_name = "posts"

urlpatterns = [
    path("", views.PostListView.as_view(), name="all_posts"),
    path("new/", views.CreatePostView.as_view(), name="create"),
    path("by/<str:username>/", views.UserPostListView.as_view(), name="for_user"),
    path("by/<str:username>/<int:pk>", views.PostDetailView.as_view(), name="single"),
    path("delete/<int:pk>/", views.DeletePostView.as_view(), name="delete"),
]
