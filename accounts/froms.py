from django import forms
from .models import *


class CustomUserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, required=True, label='', widget=forms.PasswordInput(attrs={
    }))
    password2 = forms.CharField(max_length=20, required=True, label='', widget=forms.PasswordInput(attrs={
    }))

    class Meta:
        model = CustomUser
        fields = ('username', "first_name", "last_name", 'bio', 'date_of_birth', 'photo')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("رمز ها مطابقت ندارند")
        else:
            return cd['password2']
