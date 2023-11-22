from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingСart, Subscribe, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    inlines = [IngredientAmountInline, ]


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class ShopingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingСart, ShopingCartAdmin)
