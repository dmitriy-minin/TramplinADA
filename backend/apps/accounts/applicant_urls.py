from django.urls import path
from apps.accounts.views import applicant_dashboard, applicant_profile_edit

app_name = "applicant"

urlpatterns = [
    path("", applicant_dashboard, name="dashboard"),
    path("profile/", applicant_profile_edit, name="profile_edit"),
]
