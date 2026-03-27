from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("register/applicant/", views.register_applicant_view, name="register_applicant"),
    path("register/employer/", views.register_employer_view, name="register_employer"),
    path("contact/<int:pk>/request/", views.send_contact_request, name="contact_request"),
    path("contact/<int:pk>/accept/", views.accept_contact, name="contact_accept"),
]
