from django.forms import ModelForm
from .models import Blog


class BlogsForm(ModelForm):

    class Meta:
        model = Blog
        fields = ["title", "sub_title", "description", "image", "is_published"]
        exclude = ('user',)
