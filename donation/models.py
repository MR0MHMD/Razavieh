from django.db import models


class DonationCard(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان کارت")
    image = models.ImageField(upload_to='donations/cards/', verbose_name="تصویر کارت")
    card_number = models.CharField(max_length=16, verbose_name="شماره کارت")
    sheba_number = models.CharField(max_length=30, verbose_name="شماره شبا")
    link = models.URLField(blank=True, null=True, verbose_name="لینک پرداخت یا بله")
    is_active = models.BooleanField(default=True, verbose_name="فعال است؟")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "کارت کمک مردمی"
        verbose_name_plural = "کارت‌های کمک مردمی"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
