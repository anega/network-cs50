from django import forms
from django.contrib.auth.forms import UserCreationForm

from network.models import Post, User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({"class": "form-control", "label": "", "rows": 4})
        self.fields['body'].label = ""
