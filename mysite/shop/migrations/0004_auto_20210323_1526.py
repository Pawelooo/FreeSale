# Generated by Django 3.1.3 on 2021-03-23 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_promotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='end_date',
            field=models.DateTimeField(verbose_name='Data zakończenia'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Produkt'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='promotion_type',
            field=models.SmallIntegerField(choices=[(1, 'highlight'), (2, 'bold')], verbose_name='Typ promocji'),
        ),
    ]
