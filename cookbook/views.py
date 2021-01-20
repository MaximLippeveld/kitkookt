from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.forms.models import model_to_dict
import random
from collections import Counter
import cloudinary
import json

from .models import Recipe

from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator

MAX_N = 10

def recipe_to_context(recipe):
    context = model_to_dict(recipe, exclude=["image", "date_published"])
    context["diet"] = recipe.get_diet_display()

    ingredientlists = []
    for ingredientlist in recipe.ingredientlists.all():
        ilc = model_to_dict(ingredientlist)
        ilc["ingredients"] = [model_to_dict(ingredient) for ingredient in ingredientlist.ingredients.all()]
        ingredientlists.append(ilc)

    context["ingredientlists"] = ingredientlists
    context["icon_class"] = recipe.get_diet_display().lower()

    if recipe.image.url is not None:
        coords = [int(x) for x in recipe.cropping.split(",")]

        context["header_url"] = recipe.image.image(transformation=
                dict(x=coords[0], y=coords[1], width=coords[2]-coords[0], height=coords[3]-coords[1], crop="crop"),
                width = "auto", dpr = "auto", crop = "scale", responsive = "true", responsive_placeholder = "blank", secure=True, quality=100
        )

        cloudinary.CloudinaryImage()
    else:
        context["header_url"] = False

    return context


def info(request):
    return render(request, "cookbook/info.html")


def overview(request):

    n_items = 5
    recipes = Recipe.objects.filter(published=True)

    if "pk" in request.GET:
        recipe = Recipe.objects.get(pk=request.GET["pk"])

        # sample n_items random recipes
        counts = Counter(random.choices(recipe.meal_category, k=n_items))
        selected = Recipe.objects.none()
        for k,v in counts.items():
            selected |= recipes.filter(meal_category__icontains=k).exclude(pk=recipe.pk).order_by('?')[:v]
        recipes = selected
    else:
        recipes = recipes.order_by('-date_published')
        
        if "cat" in request.GET:
            query = request.GET["cat"]
            recipes = recipes.filter(meal_category__icontains=query)
        if "q" in request.GET:
            query = request.GET["q"]
            recipes = recipes.filter(title__icontains=query)

    paginator = Paginator(recipes, n_items)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        "recipes": [recipe_to_context(recipe) for recipe in page_obj],
        "category_choices": Recipe.CATEGORY_CHOICES,
        "more_available": json.dumps(page_obj.has_next())
    }

    if request.content_type == 'application/json':    
        html = render_to_string(
            template_name="cookbook/recipe-list.html", 
            context=context
        )

        data_dict = {"html_from_view": html, "more_available": page_obj.has_next()}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, "cookbook/overview.html", context)


def recipe(request, url_title):
    recipe = Recipe.objects.get(url_title__iexact=url_title)
    context = recipe_to_context(recipe)

    if recipe.published:
        return render(
            request,
            "cookbook/recipe-detail.html",
            context
        )
    else:
        return HttpResponseNotFound()

