from typing import Any
from django.core.management.base import BaseCommand
from get_reader import get_reader

from recipes.models import Ingredients

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        reader = get_reader('data/ingredients.csv')
        next(reader, None)
        for row in reader:
            obj, created = Ingredients.objects.get_or_create(
                id=row[0],
                name=row[1],
                units=row[2]
            )
        self.stdout.write(self.style.SUCCESS('Загрузка ингредиентов прошла успешно.'))