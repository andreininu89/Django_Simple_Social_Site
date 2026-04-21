from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView
from groups.models import Group

# Create your views here.


class GroupCreateView(LoginRequiredMixin, CreateView):
    fields = ["name", "description"]
    model = Group


class SingleGroupDetailView(DetailView):
    model = Group


class SingleGroupListView(ListView):
    model = Group
