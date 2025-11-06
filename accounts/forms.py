from django.contrib.auth.password_validation import validate_password
from jalali_date.widgets import AdminJalaliDateWidget
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
from jalali_date.fields import JalaliDateField
from .models import CustomUser
from django import forms


class CustomUserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'})
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'photo')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
            'bio': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'درباره خودتان بنویسید...'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: 09121234567'})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("رمزها با هم مطابقت ندارند")
        return cd.get('password2')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
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


class OTPVerifyForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        widget=forms.HiddenInput()  # شماره موبایل مخفی است
    )
    code = forms.CharField(
        max_length=6,
        label="کد تأیید",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد ارسال شده'})
    )


class MobileLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        label="شماره موبایل",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثلاً 09121234567'})
    )


class PersianSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="رمز عبور جدید",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور جدید را وارد کنید',
            'class': 'form-input'
        }),
        help_text="رمز عبور باید حداقل ۸ کاراکتر باشد و ترکیبی از حروف و اعداد باشد."
    )

    new_password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور را دوباره وارد کنید',
            'class': 'form-input'
        }),
        help_text=""
    )

    error_messages = {
        'password_mismatch': "❌ رمزهای عبور واردشده با هم مطابقت ندارند.",
    }

    def clean_new_password1(self):
        password1 = self.cleaned_data.get("new_password1")

        # اگر هیچ پسوردی وارد نشده، اجازه بده default field validation ارور بده
        if not password1:
            return password1

        try:
            # این تابع ممکنه ValidationError با error_list داشته باشه (هر مورد دارای .message و .code)
            validate_password(password1, self.user)
        except ValidationError as e:
            # تبدیل خطاها بر اساس کد (قابل اطمینان‌تر از مقایسه متن)
            translated = []
            for err in e.error_list:
                code = getattr(err, 'code', '')
                # بر اساس کد پیام مناسب بگذار
                if code == 'password_too_short' or 'short' in code:
                    translated.append("رمز عبور باید حداقل ۸ کاراکتر باشد.")
                elif code == 'password_too_common' or 'common' in code:
                    translated.append("رمز عبور بسیار رایج است. لطفاً رمز قوی‌تری انتخاب کنید.")
                elif code == 'password_entirely_numeric' or 'numeric' in code:
                    translated.append("رمز عبور نباید فقط شامل اعداد باشد.")
                elif code == 'password_too_similar' or 'similar' in code:
                    translated.append("رمز عبور نباید مشابه نام کاربری یا اطلاعات شخصی شما باشد.")
                else:
                    # پیام عمومی برای هر مورد نامشخص
                    translated.append("رمز انتخاب‌شده ضوابط امنیتی را رعایت نمی‌کند. لطفاً رمز دیگری انتخاب کنید.")
            # حتماً فقط پیام‌های ترجمه‌شده را پرتاب کنیم — این جلوی نمایش پیام‌های انگلیسیِ اصلی را می‌گیرد
            raise ValidationError(translated, code='invalid')

        return password1
