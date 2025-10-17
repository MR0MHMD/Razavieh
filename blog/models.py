from django.db import models
from django.utils.text import slugify
from django_jalali.db import models as jmodels


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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.title))
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



