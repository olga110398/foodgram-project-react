from csv import DictReader

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Ingredient.objects.exists():
            print('Данные уже загружены!')
            return
        print('Загрузка данных ингридиентов')

        try:
            with open('recipes/data/ingredients.csv', encoding='utf-8') as f:
                reader = DictReader(f)
                for row in reader:
                    obj, created = Ingredient.objects.get_or_create(
                        name=row['name'],
                        measurement_unit=row['measurement_unit']
                    )
                print('Загрузка ингредиентов прошла успешно.')
        except FileNotFoundError:
            print('CSV file не найден.')
        except Exception as error:
            print(f'Произошла ошибка {str(error)}')
