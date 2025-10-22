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
    likes = models.PositiveIntegerField(default=0, verbose_name='تعداد لایک‌ها')
    views = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')

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


class ReportLike(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='likes_rel')
    session_key = models.CharField(max_length=40)

    class Meta:
        unique_together = ('report', 'session_key')

    def __str__(self):
        return f"Like for {self.report.title} by session {self.session_key}"


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
    like_count = models.PositiveIntegerField(default=0, verbose_name="تعداد لایک‌ها")
    dislike_count = models.PositiveIntegerField(default=0, verbose_name="تعداد دیسلایک‌ها")

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"{self.name} : {self.report}"


class CommentReaction(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='reactions')
    session_key = models.CharField(max_length=40)
    reaction_type = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')])
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'session_key')

    def __str__(self):
        return f"{self.session_key} - {self.reaction_type} ({self.comment.id})"
