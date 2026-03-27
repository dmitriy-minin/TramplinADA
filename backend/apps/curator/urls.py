from django.urls import path
from . import views

app_name = "curator"

urlpatterns = [
    path("", views.curator_dashboard, name="dashboard"),
    path("companies/", views.companies_list, name="companies"),
    path("companies/<int:pk>/verify/", views.verify_company, name="verify_company"),
    path("opportunities/", views.opportunities_moderation, name="opportunities"),
    path("opportunities/<int:pk>/moderate/", views.moderate_opportunity, name="moderate"),
    path("users/", views.users_list, name="users"),
    path("users/<int:pk>/", views.user_detail, name="user_detail"),
    path("users/<int:pk>/toggle/", views.toggle_user_active, name="toggle_user"),
    path("tags/", views.tags_list, name="tags"),
    path("tags/create/", views.tag_create, name="tag_create"),
    path("tags/<int:pk>/delete/", views.tag_delete, name="tag_delete"),
    path("curators/", views.curators_list, name="curators"),
    path("curators/create/", views.curator_create, name="curator_create"),
]
