from django_jalali.db import models as jmodels
from django.utils.text import slugify
from django.urls import reverse
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = 'پست خبری'
        verbose_name_plural = 'پست های خبری'

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.title))
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='نظر')
    name = models.CharField(max_length=250, verbose_name='نام')
    body = models.TextField(verbose_name="متن نظر")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="آخرین ویرایش")
    active = models.BooleanField(default=True, verbose_name="وضعیت")

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"{self.name} : {self.post}"
