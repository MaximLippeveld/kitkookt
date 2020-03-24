from django.db import models
from fontawesome_5.fields import IconField
from ckeditor.fields import RichTextField
from image_cropping import ImageRatioField
from cloudinary import models as cl_models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=256)
    ingredientlist = models.ForeignKey("IngredientList", on_delete=models.CASCADE, related_name="ingredients")

    def __str__(self):
        return self.name

class IngredientList(models.Model):
    name = models.CharField(max_length=100, name="name")
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="ingredientlists")

    def __str__(self):
        return self.name

class Recipe(models.Model):
    url_title = models.CharField(max_length=100)
    intro = models.TextField(name="intro")
    title = models.TextField(name="title")
    steps = RichTextField(name="steps")
    icon = IconField(default="seedling")
    image = cl_models.CloudinaryField(name="image")
    cropping = ImageRatioField('image', '1000x200') 
    published = models.BooleanField(name='published', default=False) 

    VEGAN = 1
    VEGETARIAN = 2
    DIET = (
        (VEGAN, "Vegan"),
        (VEGETARIAN, "Veggie")
    )
    diet = models.PositiveSmallIntegerField(
        choices = DIET,
        default = VEGETARIAN
    )

    def save(self, *args, **kwargs):
        if not self.url_title:
            self.url_title = list(filter(str.isalnum, self.title[:30]))
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
