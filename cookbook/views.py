from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict

from .models import Recipe

def recipe(request, url_title):
    print("localhost:8000/recept/speculaastaart")

    recipe = Recipe.objects.get(url_title__iexact=url_title)

    context = model_to_dict(recipe)
    context["icon"] = recipe.icon
    context["diet"] = recipe.get_diet_display()
    context["ingredients"] = [
        model_to_dict(ingredient)
        for ingredient in recipe.ingredients.all()
    ]
    context["icon_class"] = recipe.get_diet_display().lower()

    return render(
        request,
        "cookbook/recipe.html",
        context
    )
