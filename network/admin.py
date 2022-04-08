from django.contrib import admin

from network.models import User, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("body", "author", "created_at")


admin.site.register(User)
admin.site.register(Post, PostAdmin)
