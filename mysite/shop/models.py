from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from hitcount.models import HitCount
from django import forms


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=8, max_length=8)
    description = models.TextField(max_length=5000)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    image = models.FileField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


PROMOTION_CHOICES = (
    (1, 'highlight'),
    (2, 'bold')
)


class Promotion(models.Model):
    promotion_type = models.SmallIntegerField(choices=PROMOTION_CHOICES, verbose_name='Typ promocji')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Produkt')
    end_date = models.DateTimeField(verbose_name='Data zakończenia')

    def get_price(self):
        if self.promotion_type == PROMOTION_CHOICES[0][0]:
            return Decimal('5')
        elif self.promotion_type == PROMOTION_CHOICES[1][0]:
            return Decimal('8')
        return Decimal('10')










# ToDo Sortowanie od najnowszego albo od najstarszego

