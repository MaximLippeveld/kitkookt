from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict
from image_cropping.utils import get_backend
import urllib.request
from django.conf import settings
import os

from .models import Recipe

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def recipe_to_context(recipe):
    context = model_to_dict(recipe)
    context["diet"] = recipe.get_diet_display()
    context["ingredients"] = [
        model_to_dict(ingredient)
        for ingredient in recipe.ingredients.all()
    ]
    context["icon_class"] = recipe.get_diet_display().lower()

    img_new = os.path.join("recipe", os.path.basename(recipe.image.url))
    if not default_storage.exists(img_new):
        default_storage.save(img_new, ContentFile(urllib.request.urlopen(recipe.image.url).read()))

    context["header_url"] = get_backend().get_thumbnail_url(
        img_new,
        {
            'size': (1000, 200),
            'box': recipe.cropping,
            'crop': True,
            'detail': True,
        }
    )

    return context


def overview(request):
    recipes = Recipe.objects.all()

    context = {"recipes": [recipe_to_context(recipe) for recipe in recipes]}

    return render(request, "cookbook/overview.html", context)


def recipe(request, url_title):
    recipe = Recipe.objects.get(url_title__iexact=url_title)
    context = recipe_to_context(recipe)

    return render(
        request,
        "cookbook/recipe.html",
        context
    )
