from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingСart, Subscribe, Tag)
from users.models import CustomUser
from .filters import IngredientSearchFilter, RecipeFilter
from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeListSerializer, RecipeSerializer,
                          ShoppingCartSerializer, SubcribeSerializer,
                          SubscribeListSerializer, TagSerializer)
from .pagination import CustomPaginator


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсеты для модели Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filterset_class = IngredientSearchFilter


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсеты для модели Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """Вьюсеты для модели Recipe."""
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPaginator

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer


class SubscribeListView(ListAPIView):
    """Получение списка всех подписок на пользователей."""
    serializer_class = SubscribeListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPaginator

    def get_queryset(self):
        return CustomUser.objects.filter(following__follower=self.request.user)


class SubscribeViewSet(APIView):
    """Создает подписку/отписку на/от автора."""
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        following = get_object_or_404(CustomUser, id=kwargs['id'])
        serializer = SubcribeSerializer(
            data={'follower': request.user.id, 'following': following.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        following = get_object_or_404(CustomUser, id=kwargs['id'])
        count_delete, _ = Subscribe.objects.filter(follower=request.user,
                                                   following=following
                                                   ).delete()
        if not count_delete:
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'status': 'Успешная отписка'},
                        status=status.HTTP_204_NO_CONTENT)


class APIFavorite(APIView):
    """Добавляет/удаляет рецепт в/из избранного."""
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        serializer = FavoriteSerializer(
            data={'user': request.user.id, 'recipe': kwargs['id']},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['id'])
        count_delete, _ = Favorite.objects.filter(user=request.user,
                                                  recipe=recipe).delete()
        if not count_delete:
            return Response({'error': 'Рецепта нет в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Рецепт удален из избранного'},
                        status=status.HTTP_204_NO_CONTENT)


class APIShoppingCart(APIView):
    """Добавляет/удаляет рецепт в/из корзину."""
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        serializer = ShoppingCartSerializer(
            data={'user': request.user.id, 'recipe': kwargs['id']},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['id'])
        count_delete, _ = ShoppingСart.objects.filter(
            user=request.user,
            recipe=recipe).delete()
        if not count_delete:
            return Response({'error': 'Рецепта нет в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Рецепт удален из избранного'},
                        status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        recipe = ShoppingСart.objects.filter(user=request.user
                                             ).values_list('recipe_id')

        ingredients = IngredientAmount.objects.filter(
            recipe__in=recipe).values(
                'ingredient__name',
                'ingredient__measurement_unit').annotate(amount=Sum('amount'))
        shopping_list = ['Список покупок:']
        for ingredient in ingredients:
            name = ingredient["ingredient__name"]
            amount = ingredient["amount"]
            measurement_unit = ingredient["ingredient__measurement_unit"]
            shopping_list.append(f'\n{name} - {amount}, {measurement_unit}')
        response = FileResponse(shopping_list, content_type='text/plain')
        response['Content_Disposition'] = ('attachment; '
                                           'filename="shopping_cart.txt"')
        return response
