from django.urls import include, path
from rest_framework import routers

from .views import (IngredientViewSet, TagViewSet, RecipeViewSet,
                    SubscribeViewSet, SubscribeListView, FavoriteViewSet)
from users.views import UserViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    #path('users/subscriptions', SubscribeListView.as_view('')),
    path('users/<int:id>/subscribe', SubscribeViewSet.as_view({'post': 'subscribe',
                                                               'delete': 'subscribe'})),
    path('recipes/<int:id>/favorite', FavoriteViewSet.as_view({'post': 'favorite',
                                                               'delete': 'favorite'})),
]
