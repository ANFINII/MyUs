from django import forms
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextFormField
from .models import SearchTag, BlogModel

User = get_user_model()

class SearchTagForm(forms.ModelForm):
    class Meta:
        model = SearchTag
        fields = [
            'name',
        ]

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ('richtext',)
        widgets = {
            'richtext': RichTextFormField(),
        }
