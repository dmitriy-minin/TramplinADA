from django.urls import path
from apps.opportunities.views import api_map_markers

urlpatterns = [
    path("map-markers/", api_map_markers, name="api_map_markers"),
]
