from django import forms
from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image']
        labels = {
            'title': 'عنوان پست',
            'description': 'توضیحات',
            'image': 'تصویر شاخص',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'مثلاً: برنامه جدید مسجد برای ماه رمضان...',
                'class': 'form-input'
            }),
            'description': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'متن کامل پست را اینجا وارد کنید...',
                'class': 'form-textarea'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-file'
            })
        }


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
