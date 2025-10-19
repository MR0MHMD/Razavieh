from django_jalali.db import models as jmodels
from django_resized import ResizedImageField
from django.utils.text import slugify
from django.urls import reverse
from django.db import models


class Report(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان مراسم')
    description = models.TextField(verbose_name='توضیحات')
    slug = models.SlugField(unique=True, blank=True, null=True)
    date = jmodels.jDateField(default=None, verbose_name="تاریخ مراسم")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        ordering = ['-date']
        verbose_name = 'گزارش روز'
        verbose_name_plural = 'گزارشات روز'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('report:report_detail', args=[self.slug])

    def __str__(self):
        return self.title


class ReportImage(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='images')
    image = ResizedImageField(upload_to='reports/%Y/%m/%d/', size=(1920, 1080),
                              quality=100, crop=['middle', 'center'], verbose_name='تصویر')

    class Meta:
        verbose_name = 'تصویر گزارشات'
        verbose_name_plural = 'تصاویر گزارشات'


class Comment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=250, verbose_name='نام')
    body = models.TextField(verbose_name="متن نظر")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    active = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"{self.name} : {self.report}"
