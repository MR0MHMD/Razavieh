from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from django_jalali.db import models as jmodels


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="شماره موبایل")
    verification_code = models.CharField(max_length=6, blank=True, null=True, verbose_name="کد تأیید")
    photo = ResizedImageField(upload_to='profile_image', verbose_name='تصویر', blank=True, null=True)
    joined_jalali = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت (شمسی)")
    otp_created_at = models.DateTimeField(blank=True, null=True, verbose_name="زمان ایجاد OTP")

    def __str__(self):
        return self.username
