from django.urls import path
from .views import cards_and_brochures_view

urlpatterns = [
    path("admin/cards_and_brochures/", cards_and_brochures_view, name="cards-and-brochures"),
]
