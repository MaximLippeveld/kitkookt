from django.db import models
from fontawesome_5.fields import IconField
from ckeditor.fields import RichTextField
from image_cropping import ImageRatioField


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=256)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="ingredients")

    def __str__(self):
        return self.name

class Recipe(models.Model):
    url_title = models.CharField(max_length=100)
    intro = models.TextField(name="intro")
    title = models.TextField(name="title")
    steps = RichTextField(name="steps")
    icon = IconField(default="seedling")
    image = models.ImageField(upload_to="recipe", name="image")
    cropping = ImageRatioField('image', '500x150') 

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
