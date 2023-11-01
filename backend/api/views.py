from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets, status
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from recipes.models import Ingredient, Tag, Recipe, Subscribe, Favorite
from users.models import CustomUser
from recipes.filters import IngredientSearchFilter
from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (IngredientSerializer, TagSerializer, RecipeSerializer,
                          RecipeListSerializer, SubcribeSerializer,
                          SubscribeListSerializer, FavoriteSerializer)
from users.serializers import ProfileSerializer


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

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

class SubscribeListView(ListAPIView):
    serializer_class = SubscribeListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (CustomUser.objects.filter(following__user=self.request.user))


class SubscribeViewSet(ModelViewSet):
    """Вьюсеты для модели Subcribe."""
    queryset = CustomUser.objects.all()
    serializer_class = SubcribeSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)


    def subscribe(self, request, **kwargs):
        """Создает подписку/отписку на/от автора."""
        follower = request.user
        following_id = self.kwargs.get('id')
        following = get_object_or_404(CustomUser, id=following_id)
        if request.method == 'POST':
            serializer = ProfileSerializer(following, context={'request': request})
            Subscribe.objects.create(follower=follower, following=following)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user_follow = get_object_or_404(Subscribe,
                                            follower=follower,
                                            following=following)
            user_follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def favorite(self, request, **kwargs):
        """Добавляет/удаляет рецепт в/из избранного."""
        user = request.user
        recipe_id = self.kwargs.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.method == 'POST':
            serializer = FavoriteSerializer(recipe, context={'request': request})
            Favorite.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            recipe_favorite = get_object_or_404(Recipe,
                                            user=user,
                                            recipe=recipe)
            recipe_favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)