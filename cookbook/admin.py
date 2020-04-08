from django.contrib import admin
from .models import Recipe, Ingredient, IngredientList
from image_cropping import ImageCroppingMixin

class IngredientInline(admin.StackedInline):
    model = Ingredient
    extra = 1

class IngredientListInline(admin.StackedInline):
    model = IngredientList
    extra = 1


class IngredientListAdmin(admin.ModelAdmin):
    list_display=('name','recipe')
    inlines = [IngredientInline]
    extra = 1

class RecipeAdmin(ImageCroppingMixin, admin.ModelAdmin):
    inlines = [IngredientListInline]

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientList, IngredientListAdmin)
