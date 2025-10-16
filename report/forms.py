from django import forms
from .models import Report, ReportImage


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'date']


class ReportImageForm(forms.ModelForm):
    class Meta:
        model = ReportImage
        fields = ['image']
