from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingСart, Subscribe, Tag)
from users.models import CustomUser
from users.serializers import ProfileSerializer

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
    filter_backends = [IngredientSearchFilter]


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсеты для модели Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class RecipeViewSet(ModelViewSet):
    """Вьюсеты для модели Recipe."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPaginator

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer


class SubscribeListView(ListAPIView):
    """APIView для отображения списка подписок"""
    serializer_class = SubscribeListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        subscribe = Subscribe.objects.filter(
            follower=self.request.user).values_list('following_id')
        return CustomUser.objects.filter(id__in=subscribe)


class SubscribeViewSet(ModelViewSet):
    """Вьюсеты для модели Subcribe."""
    queryset = CustomUser.objects.all()
    serializer_class = SubcribeSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['following__username', ]
    pagination_class = CustomPaginator

    def subscribe(self, request, **kwargs):
        """Создает подписку/отписку на/от автора."""
        follower = request.user
        following_id = self.kwargs.get('id')
        following = get_object_or_404(CustomUser, id=following_id)
        if request.method == 'POST':
            serializer = ProfileSerializer(following,
                                           context={'request': request})
            Subscribe.objects.create(follower=follower, following=following)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user_follow = get_object_or_404(Subscribe,
                                            follower=follower,
                                            following=following)
            user_follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class APIFavorite(APIView):
    """Добавляет/удаляет рецепт в/из избранного."""
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['id'])
        serializer = FavoriteSerializer(recipe, context={'request': request})
        if Favorite.objects.filter(user=request.user,
                                   recipe=recipe).exists():
            return Response({'error': 'Рецепт уже добавлен в избранное'},
                            status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=request.user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['id'])
        if not Favorite.objects.filter(user=request.user,
                                       recipe=recipe).exists():
            return Response({'error': 'Рецепта нет в избранном'},
                            status=status.HTTP_400_BAD_REQUEST)

        get_object_or_404(Favorite, user=request.user,
                          recipe=recipe).delete()
        return Response({'detail': 'Рецепт удален из избранного'},
                        status=status.HTTP_204_NO_CONTENT)


class APIShoppingCart(APIView):
    """Добавляет/удаляет рецепт в/из корзину."""
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['id'])
        serializer = ShoppingCartSerializer(recipe,
                                            context={'request': request})
        if ShoppingСart.objects.filter(user=request.user,
                                       recipe=recipe).exists():
            return Response({'error': 'Рецепт уже добавлен в корзину'},
                            status=status.HTTP_400_BAD_REQUEST)
        ShoppingСart.objects.create(user=request.user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['id'])
        if not ShoppingСart.objects.filter(user=request.user,
                                           recipe=recipe).exists():
            return Response({'error': 'Рецепта нет в корзине'},
                            status=status.HTTP_400_BAD_REQUEST)

        get_object_or_404(ShoppingСart, user=request.user,
                          recipe=recipe).delete()
        return Response({'detail': 'Рецепт удален из корзины'},
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
