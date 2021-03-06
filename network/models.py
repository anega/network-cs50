from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name="followers", blank=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="posts")
    body = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, blank=True, related_name="posts_liked")

    def __str__(self):
        return f"{self.body[0:15]} {self.author} {self.created_at}"
