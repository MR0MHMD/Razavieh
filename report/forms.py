from django import forms
from .models import *


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'date']


class ReportImageForm(forms.ModelForm):
    class Meta:
        model = ReportImage
        fields = ['image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'متن نظر',
                'rows': 4,
            }),
        }
        labels = {
            'body': ''
        }
