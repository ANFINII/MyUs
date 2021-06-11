from django import forms
from django.contrib.auth import get_user_model
from django.contrib.admin import widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import SearchTag

User = get_user_model()

class SearchTagForm(forms.ModelForm):
    class Meta:
        model = SearchTag
        fields = [
            'searchtag',
        ]