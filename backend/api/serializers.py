import base64

import webcolors
from django.core.files.base import ContentFile
from rest_framework import serializers, status
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingСart, Subscribe, Tag)
from users.models import CustomUser
from users.serializers import ProfileSerializer


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('name', 'measurement_unit')
        model = Ingredient


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')
        model = Tag


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = IngredientAmount


class RecipeListSerializer(serializers.ModelSerializer):

    author = ProfileSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True,
                                             source='ingredient_amount')
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')
        model = Recipe

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user,
                                       recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingСart.objects.filter(user=user,
                                           recipe=obj).exists()


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1,)

    class Meta:
        fields = ('id', 'amount')
        model = IngredientAmount


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):

    ingredients = AddIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    image = Base64ImageField()

    class Meta:
        fields = ('ingredients', 'tags', 'name',
                  'text', 'cooking_time', 'image')
        model = Recipe

    def validate(self, data):
        tags = data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Нужно выбрать хотя бы один тег!'})
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError({'tags': 'Теги не уникальны!'})
        ingredients = data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients': 'Нужно выбрать ингердиенты!'})
        items = []
        for item in ingredients:
            items.append(item['id'])
        if len(items) != len(set(items)):
            raise serializers.ValidationError(
                {'ingredients': 'Ингредиенты не уникальны!'})
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        serializer = RecipeListSerializer(
            instance,
            context={'request': request})
        return serializer.data

    def tags_and_ingredients_set(self, recipe, tags, ingredients):
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientAmount.objects.bulk_create([
                IngredientAmount(
                    recipe=recipe,
                    ingredient=ingredient.get('id'),
                    amount=ingredient.get('amount'),)
            ])

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)

        for ingredients in ingredients_data:
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=ingredients.get('id'),
                amount=ingredients.get('amount'))
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        IngredientAmount.objects.filter(
            recipe=instance,
            ingredient__in=instance.ingredients.all()).delete()
        self.tags_and_ingredients_set(instance, tags, ingredients)
        instance.save()
        return instance


class RecipeMiniFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeListSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj)
        if limit:
            recipes = recipes[:int(limit)]
        return RecipeMiniFieldSerializer(
            recipes,
            many=True,
            context=self.context).data

    def get_recipes_count(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return recipes.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(follower=user,
                                        following=obj).exists()


class SubcribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('follower', 'following'),
                message='Вы уже подписаны на этого пользователя'
            )
        ]

    def validate(self, data):
        request = self.context.get('request')
        if request.user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя!'
            )
        if request.user.is_anonymous:
            return Response(
                {'errors':
                 'Подписаться можно только авторизованным пользователям'},
                status=status.HTTP_401_UNAUTHORIZED)
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return SubscribeListSerializer(
            instance.following, context={'request': request}
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = RecipeMiniFieldSerializer(many=True, read_only=True)

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message='Рецепт уже добавлен в избранное'
            )
        ]

    def validate_recipe(self, value):
        """Проверка, что свой рецепт нельзя добавить в избранное"""
        if self.context['request'].user == value.author:
            raise serializers.ValidationError(
                'Нельзя добавить в избранное свой рецепт!'
            )
        return value

    def to_representation(self, instance):

        return RecipeMiniFieldSerializer(
            instance,
            context=self.context).data


class ShoppingCartSerializer(serializers.ModelSerializer):

    recipe = RecipeMiniFieldSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingСart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingСart.objects.all(),
                fields=['user', 'recipe'],
                message='Рецепт уже добавлен в корзину'
            )
        ]

    def to_representation(self, instance):

        return RecipeMiniFieldSerializer(instance,
                                         context=self.context).data
