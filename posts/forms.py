from django import forms
from .models import *



class PostCreateForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['title', 'short_desc', 'content', 'image']
