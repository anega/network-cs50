from django import forms

from network.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({"class": "form-control", "label": "", "rows": 4})
        self.fields['body'].label = ""
