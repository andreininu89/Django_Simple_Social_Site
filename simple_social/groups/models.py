from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

import misaka

User = get_user_model()


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default="")
    description_html = models.TextField(editable=False, blank=True, default="")
    members = models.ManyToManyField(User, through="GroupMember", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})

    class Meta:
        ordering = [
            "name",
        ]


class GroupMember(models.Model):
    group = models.ForeignKey(
        Group, related_name="memberships", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, related_name="user_groups", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "group"], name="unique_user_group")
        ]
