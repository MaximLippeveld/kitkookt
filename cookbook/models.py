from django.db import models
from fontawesome_5.fields import IconField
from ckeditor.fields import RichTextField
from image_cropping import ImageRatioField
from cloudinary import models as cl_models
from multiselectfield import MultiSelectField


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
    intro = RichTextField(name="intro")
    title = models.TextField(name="title")
    steps = RichTextField(name="steps")
    icon = IconField(default="seedling")
    image = cl_models.CloudinaryField(blank=True, name="image")
    cropping = ImageRatioField('image', '1000x200') 
    published = models.BooleanField(name='published', default=False)
    date_published = models.DateTimeField(name="date_published", null=True, blank=True)
    prep_time = models.DurationField(name="prep_time", null=True, blank=True)

    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3
    DESSERT = 4
    CATEGORY_CHOICES = (
        (BREAKFAST, "Ontbijt"),
        (LUNCH, "Lunch"),
        (DINNER, "Avondmaal"),
        (DESSERT, "Dessert")
    )
    meal_category = MultiSelectField(name="meal_category", choices=CATEGORY_CHOICES, null=True, blank=True) 

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

        # remove trailing stuff
        self.steps = self.steps[:self.steps.rfind("</p>")+4]
        self.intro = self.intro[:self.intro.rfind("</p>")+4]
        
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
