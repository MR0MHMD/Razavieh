from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_jalali.db import models as jmodels
from django_resized import ResizedImageField
from taggit.managers import TaggableManager


class Notification(models.Model):
    title = models.CharField("عنوان اطلاعیه", max_length=200)
    content = models.TextField("متن اطلاعیه")
    datetime = models.CharField("تاریخ و ساعت برگزاری")
    date = jmodels.jDateField('تاریخ برگزاری مراسم')
    location = models.CharField("محل برگزاری", max_length=255)
    is_active = models.BooleanField("فعال باشد؟", default=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(verbose_name="تگ‌ها", help_text="تگ‌ها را با کاما (,) جدا کنید")
    image = ResizedImageField(
        upload_to='notifications',
        quality=85,
        verbose_name='تصویر',
        size=[600, 800],
        keep_meta=False
    )

    class Meta:
        ordering = ['-datetime']
        verbose_name = "اطلاعیه"
        verbose_name_plural = "اطلاعیه‌ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notification:notification_detail', args=[self.pk])
