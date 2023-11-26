from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .constants import MAX_LENGHT, MIN_VALUE, MAX_VALUE
from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_LENGHT,
        verbose_name='Название ингредиента')
    measurement_unit = models.CharField(
        max_length=MAX_LENGHT,
        verbose_name='Единицы измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=MAX_LENGHT,
        verbose_name='Название тега')
    color = ColorField(
        default='#FF0000',
        verbose_name='Цветовой код')
    slug = models.SlugField(
        max_length=MAX_LENGHT,
        unique=True,)

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
        max_length=MAX_LENGHT,
        verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингердиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                MIN_VALUE,
                f'Время приготовления не может быть меньше '
                f'{MIN_VALUE} минуты'),
            MaxValueValidator(
                MAX_VALUE,
                f'Время приготовления не может быть больше {MAX_VALUE} минут')
        ]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredient_amount',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredient_amount',
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        help_text='Укажите количество ингредиента',
        blank=True,
        validators=[
            MinValueValidator(
                MIN_VALUE,
                f'Количество ингредиента не может быть меньше {MIN_VALUE}'),
            MaxValueValidator(
                MAX_VALUE,
                f'Количество ингредиента не может быть больше {MAX_VALUE}')
        ]
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
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follower_following'
            ),
            models.CheckConstraint(
                check=~models.Q(follower=models.F('following')),
                name='prevent_self_follow'
            )
        ]

    def __str__(self):
        return f'{self.follower} подписан на {self.following}'


class BaseModel(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        related_name='%(class)ss',
        verbose_name='Избранный рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class Favorite(BaseModel):

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в избраннное'


class ShoppingСart(BaseModel):

    class Meta:
        verbose_name = 'Cписок покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в список покупок'
