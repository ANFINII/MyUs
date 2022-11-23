from django import forms
from django.contrib.auth import get_user_model
from apps.myus.models import SearchTag

User = get_user_model()

class SearchTagForm(forms.ModelForm):
    class Meta:
        model = SearchTag
        fields = ['name']
