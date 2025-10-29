from django.db import models
from django_jalali.db import models as jmodels


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
