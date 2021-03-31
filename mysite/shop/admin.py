from django.contrib import admin

from shop.models import Category, Product, Promotion

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Promotion)
