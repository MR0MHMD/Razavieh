from django import forms
from .models import Notification
from django_jalali.forms import jDateField
from django_jalali.admin.widgets import AdminjDateWidget


class NotificationForm(forms.ModelForm):
    date = jDateField(widget=AdminjDateWidget(
        attrs={'placeholder': 'YYYY-MM-DD'}))
    class Meta:
        model = Notification
        fields = ['title', 'content', 'datetime', 'location', 'date', 'is_active', 'tags', 'image']
        labels = {
            'title': 'عنوان اطلاعیه',
            'content': 'متن اطلاعیه',
            'location': 'محل برگزاری',
            'is_active': 'فعال باشد؟',
            'tags': 'تگ‌ها',
            'image': 'تصویر اطلاعیه',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'عنوان اطلاعیه را وارد کنید'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 6,
                'placeholder': 'متن اطلاعیه را اینجا بنویسید...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'مثلاً: مسجد رضویه - خیابان امام خمینی'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'تگ‌ها را با کاما (,) جدا کنید'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }
