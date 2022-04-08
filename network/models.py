from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="posts")
    body = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    last_edit = models.DateTimeField(auto_now=True, blank=False, null=False)
    like = models.ManyToManyField(User, related_name="posts_liked")

    def __str__(self):
        return f"{self.body[0:15]} {self.author} {self.created_at}"
