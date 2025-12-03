from django.db import models
from django_resized import ResizedImageField
from django_jalali.db import models as jmodels
from slugify import slugify


class Ticket(models.Model):
    subject = models.CharField(verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    name = models.CharField(max_length=250, verbose_name='نام')
    phone = models.CharField(max_length=11, verbose_name="شماره تماس")
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def __str__(self):
        return self.name


class HeroImage(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to="hero/")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title or f"Hero #{self.id}"


class Staff(models.Model):
    name = models.CharField("نام خادم", max_length=120)
    role = models.CharField("سمت / مسئولیت", max_length=200)
    slug = models.SlugField("اسلاگ", unique=True, blank=True)

    image = ResizedImageField(
        upload_to="staff/",
        size=[600, 600],
        quality=85,
        crop=['middle', 'center'],
        verbose_name="تصویر خادم",
        keep_meta=False
    )

    order = models.PositiveIntegerField("ترتیب نمایش", default=0)
    is_active = models.BooleanField("فعال باشد؟", default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "خادم مسجد"
        verbose_name_plural = "خادمان مسجد"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.replace(" ", "-"))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
