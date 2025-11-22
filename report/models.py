from django_jalali.db import models as jmodels
from django_resized import ResizedImageField
from accounts.models import CustomUser
from django.urls import reverse
from django.db import models
from main.utils import *


class Report(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان مراسم')
    description = models.TextField(verbose_name='توضیحات')
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    date = jmodels.jDateField(default=None, verbose_name="تاریخ مراسم")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    likes = models.PositiveIntegerField(default=0, verbose_name='تعداد لایک‌ها')
    views = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')
    tags = models.ManyToManyField("Tag", related_name='reports', blank=True, verbose_name='برچسب ها')
    categories = models.ManyToManyField("Category", related_name='reports', blank=True, verbose_name='دسته‌ها')

    class Meta:
        ordering = ['-date']
        verbose_name = 'گزارش روز'
        verbose_name_plural = 'گزارشات روز'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_english_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('report:report_detail', args=[self.id, self.slug])

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته')
    slug = models.SlugField(max_length=120, blank=True, null=True)

    seo_title = models.CharField(max_length=150, blank=True, null=True, verbose_name="عنوان سئو")
    seo_description = models.TextField(blank=True, null=True, verbose_name="توضیحات سئو")

    class Meta:
        verbose_name = 'دسته'
        verbose_name_plural = 'دسته‌ها'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('report:report_list_category', args=[self.id, self.slug])


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام برچسب")
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    seo_title = models.CharField(max_length=150, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'برچسب گزارش'
        verbose_name_plural = 'برچسب های گزارشات'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_english_slug(self.name)
        if not self.seo_title:
            self.seo_title = self.name
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('report:report_list_tag', args=[self.id, self.slug])

    def __str__(self):
        return self.name


class ReportLike(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='likes_rel')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='report_likes')

    class Meta:
        unique_together = ('report', 'user')
        verbose_name = 'لایک گزارش'
        verbose_name_plural = 'لایک‌های گزارش'

    def __str__(self):
        return f"Like for {self.report.title} by {self.user.username}"


class ReportImage(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='images')
    image = ResizedImageField(upload_to='reports/%Y/%m/%d/',
                              quality=85, verbose_name='تصویر',
                              size=[800, 600], keep_meta=False)

    class Meta:
        verbose_name = 'تصویر گزارشات'
        verbose_name_plural = 'تصاویر گزارشات'


class Comment(models.Model):
    report = models.ForeignKey('Report', on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
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
        return f"{self.name.get_full_name() or self.name.username} : {self.report}"


class CommentReaction(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='comment_reactions')
    reaction_type = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')])
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.reaction_type} ({self.comment.id})"
