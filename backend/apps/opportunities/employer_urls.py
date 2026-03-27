from django.urls import path
from apps.opportunities.views import (
    employer_dashboard, opportunity_create, opportunity_edit,
    employer_applicants, update_application_status, employer_company_edit,
)

app_name = "employer"

urlpatterns = [
    path("", employer_dashboard, name="dashboard"),
    path("company/", employer_company_edit, name="company_edit"),
    path("create/", opportunity_create, name="create"),
    path("<int:pk>/edit/", opportunity_edit, name="edit"),
    path("<int:pk>/applicants/", employer_applicants, name="applicants"),
    path("application/<int:app_id>/status/", update_application_status, name="update_status"),
]
