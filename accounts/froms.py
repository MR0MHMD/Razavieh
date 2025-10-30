from django import forms
from .models import CustomUser
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


class CustomUserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'})
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور'})
    )
    date_of_birth = JalaliDateField(
        label='تاریخ تولد',
        widget=AdminJalaliDateWidget,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'bio', 'date_of_birth', 'photo')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'درباره خودتان بنویسید...'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'username': 'نام کاربری'
        }

        help_texts = {
            'username': None,
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("رمزها با هم مطابقت ندارند")
        return cd.get('password2')


class UserEditForm(forms.ModelForm):
    date_of_birth = JalaliDateField(
        label='تاریخ تولد',
        widget=AdminJalaliDateWidget,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'bio', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'درباره خودتان بنویسید...'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'username': 'نام کاربری'
        }

        help_texts = {
            'username': None,
        }
