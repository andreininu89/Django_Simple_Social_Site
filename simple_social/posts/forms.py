from django import forms
from .models import Post
from groups.models import Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("message", "group")

    def __init__(self, *args, **kwargs):
        # We take the 'user' as an extra argument so we can filter groups
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes
        self.fields["message"].widget.attrs.update(
            {"class": "form-control", "placeholder": "What's on your mind?"}
        )
        self.fields["group"].widget.attrs.update({"class": "form-select"})

        # Only show groups the user has joined
        if user:
            self.fields["group"].queryset = Group.objects.filter(members=user)
