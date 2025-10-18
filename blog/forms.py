from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'متن نظر'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'نام و نام خانوادگی'
            })
        }
        labels = {
            'name': "",
            'body': ''
        }
