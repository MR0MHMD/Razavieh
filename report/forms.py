from jalali_date.widgets import AdminJalaliDateWidget
from jalali_date.fields import JalaliDateField
from django import forms
from .models import *


class ReportForm(forms.ModelForm):
    date = JalaliDateField(
        label='تاریخ مراسم',
        widget=AdminJalaliDateWidget,
        required=False
    )
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False,
                                                widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Report
        fields = ['title', 'description', 'date', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-outline',
                'placeholder': 'عنوان گزارش را وارد کنید'
            }),
            'description': forms.Textarea(attrs={
                'class': 'input-outline',
                'placeholder': 'توضیحات گزارش...'
            }),
            'date': forms.TextInput(attrs={
                'class': 'jalali-date input-outline',
                'placeholder': 'تاریخ گزارش را انتخاب کنید'
            }),
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
