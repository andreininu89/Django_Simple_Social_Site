from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views import generic
from groups.models import Group, GroupMember
from django.db import IntegrityError

# Create your views here.


class GroupCreateView(LoginRequiredMixin, CreateView):
    fields = ["name", "description"]
    model = Group


class SingleGroupDetailView(DetailView):
    model = Group


class SingleGroupListView(ListView):
    model = Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get("slug"))
        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(
                self.request, ("Warning, already a member of {}".format(group.name))
            )
        else:
            messages.success(self.request, "You are now a member!")
        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(
                user=self.request.user, group__slug=self.kwargs.get("slug")
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request, "You aren't in this group!")
        else:
            membership.delete()
            messages.success(self.request, "You have left the group.")
        return super().get(request, *args, **kwargs)
