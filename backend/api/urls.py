from django.urls import include, path
from rest_framework import routers

from users.views import UserViewSet
from .views import (APIFavorite, APIShoppingCart, IngredientViewSet,
                    RecipeViewSet, SubscribeListView, SubscribeViewSet,
                    TagViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('users/subscriptions/', SubscribeListView.as_view()),
    path('users/<int:id>/subscribe/', SubscribeViewSet.as_view()),
    path('recipes/<int:id>/favorite/', APIFavorite.as_view()),
    path('recipes/<int:id>/shopping_cart/', APIShoppingCart.as_view()),
    path('recipes/download_shopping_cart/', APIShoppingCart.as_view()),
    path('', include(router.urls)),
]
