from colorfield.fields import ColorField
from django.core.validators import RegexValidator
from django.db import models

from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название ингредиента')
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единицы измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега')
    color_code = ColorField(
        default='#FF0000',
        verbose_name='Цветовой код')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[
            RegexValidator(r'^[-a-zA-Z0-9_]+$'),
        ],
        )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        related_name='resipe',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=True,
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        through='IngredientAmount',
        verbose_name='Ингердиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        related_name='recipe',
        verbose_name='Теги'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredient_amount',
        verbose_name='Рецепт',
        null=False,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredient_amount',
        verbose_name='Ингредиент',
        null=False,
        on_delete=models.DO_NOTHING
    )
    amount = models.IntegerField(
        verbose_name='Количество ингредиента',
        help_text='Укажите количество ингредиента',
        blank=True
    )

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'


class Subscribe(models.Model):
    follower = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик')
    following = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.follower} подписан на {self.following}'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        verbose_name='Избранный рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        list_recipes = [item['name'] for item in self.recipe.values('name')]
        list_recipes_str = ', '.join(list_recipes)
        return f'{self.user} добавил {list_recipes_str} в избранные.'


class ShoppingСart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_carts',
        verbose_name='Рецепт в списке покупок',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Рецепт в список покупок'
        verbose_name_plural = 'Рецепты в списке покупок'

    def __str__(self):
        list_recipes = [item['name'] for item in self.recipe.values('name')]
        list_recipes_str = ', '.join(list_recipes)
        return f'{self.user} добавил {list_recipes_str} в список покупок.'
