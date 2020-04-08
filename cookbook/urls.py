from django.urls import path
from cookbook import views
app_name="cookbook"
urlpatterns = [
    path("recept/<str:url_title>", views.recipe, name="recipe"),
    path("recepten", views.overview, name="recipes"),
    path("", views.overview, name="recipes"),
    path("info", views.info, name="info"),
]
