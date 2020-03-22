from django.urls import path
from cookbook import views

urlpatterns = [
    path("recept/<str:url_title>", views.recipe, name="recipe"),
]
