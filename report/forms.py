from django import forms
from .models import *


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'date', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان گزارش را وارد کنید'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'توضیحات گزارش را بنویسید'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'تگ‌ها را با کاما جدا کنید'
            }),
        }
        labels = {
            'title': 'عنوان گزارش',
            'description': 'توضیحات',
            'date': 'تاریخ مراسم',
            'tags': 'تگ‌ها',
        }


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
