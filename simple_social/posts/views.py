from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from braces.views import SelectRelatedMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404

from posts import models
from posts.forms import PostForm

User = get_user_model()

# Create your views here.


class PostListView(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "group")


class UserPostListView(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"
    post_user = None

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs["username"]
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return models.Post.objects.filter(user=self.post_user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetailView(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs["username"])


class CreatePostView(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    form_class = PostForm
    model = models.Post

    def get_initial(self):
        initial = super().get_initial()
        # Look for the 'slug' from the URL
        group_slug = self.kwargs.get("slug")
        if group_slug:
            # Find the group and set it as the initial value for the dropdown
            group = get_object_or_404(models.Group, slug=group_slug)
            initial["group"] = group
        return initial

    def get_form_kwargs(self):
        # This sends the logged-in user to the form's __init__
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object: models.Post = form.save(commit=False)
        self.object.user = self.request.user

        # Security Check: Ensure user is in the group they are posting to
        selected_group = self.object.group
        if selected_group:
            is_member = selected_group.members.filter(id=self.request.user.id).exists()
            if not is_member:
                messages.error(
                    self.request, "You must join the group before you can post!"
                )
                return self.form_invalid(form)

        self.object.save()
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all_posts")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post was deleted successfully")
        return super().delete(*args, **kwargs)
