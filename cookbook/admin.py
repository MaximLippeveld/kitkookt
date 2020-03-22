from django.contrib import admin
from .models import Recipe, Ingredient
from image_cropping import ImageCroppingMixin

class IngredientInline(admin.StackedInline):
    model = Ingredient
    extra = 1

class RecipeAdmin(ImageCroppingMixin, admin.ModelAdmin):
    inlines = [IngredientInline]

admin.site.register(Recipe, RecipeAdmin)
