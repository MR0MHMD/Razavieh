from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from django_jalali.db import models as jmodels
from django.db import models


class CustomUser(AbstractUser):
    date_of_birth = jmodels.jDateField(null=True, blank=True, verbose_name="تاریخ تولد")
    bio = models.TextField(verbose_name='بیوگرافی', blank=True, null=True)
    photo = ResizedImageField(upload_to='profile_image', verbose_name='تصویر', blank=True, null=True)
    joined_jalali = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت (شمسی)")

    def __str__(self):
        return self.username
