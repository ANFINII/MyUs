from ckeditor.fields import RichTextFormField
from django import forms
from django.contrib.auth import get_user_model
from apps.myus.models import SearchTag, Blog

User = get_user_model()

class SearchTagForm(forms.ModelForm):
    class Meta:
        model = SearchTag
        fields = [
            'name',
        ]

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('richtext',)
        widgets = {
            'richtext': RichTextFormField(),
        }
