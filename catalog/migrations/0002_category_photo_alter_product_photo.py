# Generated by Django 4.2.5 on 2023-09-28 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='catalog/', verbose_name='изображение'),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='catalog/', verbose_name='изображение'),
        ),
    ]
