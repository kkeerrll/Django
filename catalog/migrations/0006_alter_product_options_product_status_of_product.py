# Generated by Django 4.2.5 on 2023-10-24 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_product_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('set_status_of_product', 'Can set status_of_product'), ('set_text', 'Can text'), ('set_category', 'Can set category')], 'verbose_name': 'продукт', 'verbose_name_plural': 'продукты'},
        ),
        migrations.AddField(
            model_name='product',
            name='status_of_product',
            field=models.BooleanField(default=False, verbose_name='опубликовано'),
        ),
    ]
