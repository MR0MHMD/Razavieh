from django_jalali.db import models as jmodels
from django_resized import ResizedImageField
from main.utils import generate_english_slug
from django.urls import reverse
from django.db import models


class Notification(models.Model):
    title = models.CharField("عنوان اطلاعیه", max_length=200)
    slug = models.SlugField('اسلاگ', max_length=200)
    content = models.TextField("متن اطلاعیه")
    datetime = models.CharField("تاریخ و ساعت برگزاری")
    date = jmodels.jDateField('تاریخ برگزاری مراسم')
    location = models.CharField("محل برگزاری", max_length=255)
    is_active = models.BooleanField("فعال باشد؟", default=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField("Tag", related_name='notification', blank=True, verbose_name='برچسب ها')
    image = ResizedImageField(
        upload_to='notifications',
        quality=85,
        verbose_name='تصویر',
        size=[600, 800],
        keep_meta=False
    )

    class Meta:
        ordering = ['-date']
        verbose_name = "اطلاعیه"
        verbose_name_plural = "اطلاعیه‌ها"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_english_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notification:notification_detail', args=[self.id, self.slug])


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام برچسب")
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "برچسب اطلاعیه"
        verbose_name_plural = "برچسب های اطلاعیه"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_english_slug(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('notification:notification_list_by_tags', args=[self.id, self.slug])

    def __str__(self):
        return self.name
