from jalali_date.widgets import AdminJalaliDateWidget
from jalali_date.fields import JalaliDateField
from .models import Notification
from django import forms


class NotificationForm(forms.ModelForm):
    date = JalaliDateField(widget=AdminJalaliDateWidget(
        attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Notification
        fields = ['title', 'content', 'datetime', 'location', 'date', 'is_active', 'image']
        labels = {
            'title': 'عنوان اطلاعیه',
            'content': 'متن اطلاعیه',
            'location': 'محل برگزاری',
            'is_active': 'فعال باشد؟',
            'image': 'تصویر اطلاعیه',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 6}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }