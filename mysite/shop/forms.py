import datetime
from urllib import request

from django.contrib.admin import widgets
from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateTimeField

from shop import models
from shop.models import Promotion, Product
from django import forms
from django.utils.translation import ugettext_lazy as _


class PromotionCreateForm(ModelForm):
    class Meta:
        model = Promotion
        fields = '__all__'
        widgets = {
            'end_date': forms.DateInput(format='%m/%d/%Y',
                                        attrs={'class': 'form-control', 'placeholder': 'Wybierz date', 'type': 'date'})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PromotionCreateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['product'].queryset = Product.objects.filter(user=user)
