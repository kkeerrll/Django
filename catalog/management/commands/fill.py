from django.core.management import BaseCommand
from catalog.models import Category
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()
        cursor = connection.cursor()
        cursor.execute("ALTER SEQUENCE catalog_category_pk RESTART WITH 1;")

        category_list = [
            {'name': 'Овощи', 'text': ''},
            {'name': 'Фрукты', 'text': ''},
            {'name': 'Крупы', 'text': ''},
            {'name': 'Кондитерские изделия', 'text': ''},
            {'name': 'Напитки', 'text': ''}
        ]
        category_for_create = []
        for category_item in category_list:
            category_for_create.append(Category(**category_item))

        Category.objects.bulk_create(category_for_create)
