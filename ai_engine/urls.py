from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health, name="ai_health"),
    path("preview/", views.preview, name="ai_preview"),
    path("publish/<int:pk>/", views.publish, name="ai_publish"),
]
