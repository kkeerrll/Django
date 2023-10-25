from django.db import models
from django.conf import settings

NULLABALE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    text = models.TextField(**NULLABALE, verbose_name='описание')
    photo = models.ImageField(upload_to='catalog/', **NULLABALE, verbose_name='изображение')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    text = models.TextField(verbose_name='описание')
    photo = models.ImageField(upload_to='catalog/', **NULLABALE, verbose_name='изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.IntegerField(verbose_name='цена')
    data = models.DateField(verbose_name='дата')
    last_modified = models.DateField(verbose_name='дата последнего изменения')

    status_of_product = models.BooleanField(default=False, verbose_name='опубликовано')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец', **NULLABALE)

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

        permissions = [
            (
                'set_status_of_product',
                'Can set status_of_product'
            ),
            (
                'set_text',
                'Can text'
            ),
            (
                'set_category',
                'Can set category'
            )

        ]


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    slug = models.CharField(max_length=100, verbose_name='slug', **NULLABALE)
    description = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='catalog/', **NULLABALE, verbose_name='изображение')
    creation_data = models.DateField(verbose_name='дата')
    sign_publication = models.BooleanField(default=True, verbose_name='признак публикации')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.title} ({self.description})'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    number = models.IntegerField(verbose_name='номер версии')
    name = models.CharField(max_length=150, verbose_name='название версии', **NULLABALE)

    is_active = models.BooleanField(default=True, verbose_name='активна')

    def __str__(self):
        return f'{self.product} версия {self.number} ({self.is_active})'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
