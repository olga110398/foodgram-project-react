from django.contrib import admin

from .models import Ingredient, Tag, Recipe, IngredientAmount, Subscribe, Favorite


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    inlines = [IngredientAmountInline, ]

class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')

class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
