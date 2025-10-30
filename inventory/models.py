from django.urls import reverse
from django_jalali.db import models as jmodels
from django_resized import ResizedImageField
from django.db import models


class Scrotter(models.Model):
    EVENTS_CHOICES = [
        ('شهادت', 'شهادت'),
        ('ولادت', 'ولادت'),
        ('همه مناسبت ها', 'همه مناسبت ها'),
    ]

    text = models.CharField(max_length=200, verbose_name="متن پارچه")
    category = models.CharField(max_length=50, choices=EVENTS_CHOICES, verbose_name="مناسبت")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    location = models.CharField(max_length=500, verbose_name="محل نگهداری")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    last_used = jmodels.jDateField(verbose_name="آخرین استفاده", null=True, blank=True)
    width = models.PositiveIntegerField(verbose_name="عرض", null=True, blank=True)
    height = models.PositiveIntegerField(verbose_name="ارتفاع", null=True, blank=True)
    image = ResizedImageField(upload_to=f"inventory", size=[800, 600],
                              null=True, blank=True, quality=70)

    class Meta:
        verbose_name = "پارچه"
        verbose_name_plural = "پارچه ها"
        ordering = ['category', 'text']

    def get_absolute_url(self):
        return reverse('inventory:scrotter_detail', args=[self.id])

    def __str__(self):
        return f"{self.text}"


class Decorative(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام")
    description = models.TextField(max_length=500, verbose_name='توضیحات')
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    last_used = jmodels.jDateField(verbose_name="آخرین استفاده", null=True, blank=True)
    location = models.CharField(max_length=500, verbose_name="محل نگهداری")
    image = ResizedImageField(upload_to=f"inventory", size=[800, 600],
                              null=True, blank=True, quality=70)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = "دکوری"
        verbose_name_plural = "دکوری ها"

    def get_absolute_url(self):
        return reverse('inventory:decorative_detail', args=[self.id])

    def __str__(self):
        return f"{self.name}"
