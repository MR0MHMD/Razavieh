from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from django.db import models


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")
    bio = models.TextField(verbose_name='بیوگرافی', blank=True, null=True)
    photo = ResizedImageField(upload_to='profile_image', verbose_name='تصویر', blank=True, null=True)
