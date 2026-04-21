from django.contrib import admin
from . import models


# 1. This allows editing members directly inside the Group page
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember
    extra = 1  # Provides 1 empty row to add a new member quickly


# 2. This configures the Group page with slugs and inlines
class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [GroupMemberInline]


# 3. This makes the separate Member list easier to read
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "group")
    list_filter = ("group",)  # Adds a sidebar filter by group


# Register everything
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.GroupMember, GroupMemberAdmin)
