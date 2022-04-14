from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from network.forms import CustomUserCreationForm
from network.models import User, Post


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        ("User following list", {
            "fields": ("following",)
        })
    )


class PostAdmin(admin.ModelAdmin):
    list_display = ("body", "author", "created_at")


admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
