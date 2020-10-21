from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.forms.models import model_to_dict
from image_cropping.utils import get_backend
import urllib.request
from django.conf import settings
import os
import random
from collections import Counter

from .models import Recipe

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django.http import JsonResponse

MAX_N = 10

def recipe_to_context(recipe):
    context = model_to_dict(recipe)
    context["diet"] = recipe.get_diet_display()

    # if len(context["meal_category"]) > 0:
    #     context["category_display"] = Recipe.CATEGORY_CHOICES[int(context["meal_category"][0])][1]
    # else:
    #     context["category_display"] = ""

    ingredientlists = []
    for ingredientlist in recipe.ingredientlists.all():
        ilc = model_to_dict(ingredientlist)
        ilc["ingredients"] = [model_to_dict(ingredient) for ingredient in ingredientlist.ingredients.all()]
        ingredientlists.append(ilc)

    context["ingredientlists"] = ingredientlists
    context["icon_class"] = recipe.get_diet_display().lower()

    if recipe.image.url is not None:
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
            q = recipes.filter(meal_category__icontains=k).exclude(pk=recipe.pk).all()
            # n_avail = q.count()
            selected |= q[:v]
        recipes = selected
    else:
        recipes = recipes.order_by('-date_published')
        
        if "cat" in request.GET:
            query = request.GET["cat"]
            recipes = recipes.filter(meal_category__icontains=query)
        if "q" in request.GET:
            query = request.GET["q"]
            recipes = recipes.filter(title__icontains=query)

        if "page" in request.GET:
            page = int(request.GET["page"])
        else:
            page = 1

        end = page*n_items
        recipes = recipes[:end]

    context = {
        "recipes": [recipe_to_context(recipe) for recipe in recipes],
        "category_choices": Recipe.CATEGORY_CHOICES
    }

    if request.content_type == 'application/json':    
        html = render_to_string(
            template_name="cookbook/recipe-list.html", 
            context=context
        )

        data_dict = {"html_from_view": html, "more_available": True}
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

