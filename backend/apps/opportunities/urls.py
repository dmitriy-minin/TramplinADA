from django.urls import path
from . import views

urlpatterns = [
    path("", views.opportunity_list, name="opportunity_list"),
    path("<int:pk>/", views.opportunity_detail, name="opportunity_detail"),
    path("<int:pk>/apply/", views.apply_opportunity, name="apply_opportunity"),
    path("<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
]
