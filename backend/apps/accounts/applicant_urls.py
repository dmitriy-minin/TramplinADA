from django.urls import path
from apps.accounts.views import applicant_dashboard, applicant_profile_edit, applicants_catalog

app_name = "applicant"

urlpatterns = [
    path("", applicant_dashboard, name="dashboard"),
    path("profile/", applicant_profile_edit, name="profile_edit"),
    path("catalog/", applicants_catalog, name="catalog"),
]
