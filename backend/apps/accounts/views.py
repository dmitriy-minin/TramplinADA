from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import User
from .forms import LoginForm, RegisterApplicantForm, RegisterEmployerForm, ApplicantProfileForm
from apps.companies.models import Company
from apps.companies.forms import CompanyProfileForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next", "dashboard")
            return redirect(next_url)
        else:
            messages.error(request, "Неверный email или пароль.")

    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    role = request.GET.get("role", "applicant")
    return render(request, "accounts/register_choose.html", {"role": role})


def register_applicant_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterApplicantForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Добро пожаловать на Трамплин! Заполните профиль.")
        return redirect("dashboard")
    return render(request, "accounts/register_applicant.html", {"form": form})


def register_employer_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterEmployerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        # Create company
        Company.objects.create(
            owner=user,
            name=form.cleaned_data["company_name"],
            corporate_email=form.cleaned_data["corporate_email"],
            inn=form.cleaned_data.get("inn", ""),
            status=Company.STATUS_PENDING,
        )
        login(request, user)
        messages.success(request, "Аккаунт создан. Верификация компании займёт до 24 часов.")
        return redirect("dashboard")
    return render(request, "accounts/register_employer.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard_view(request):
    user = request.user
    if user.is_curator:
        return redirect("curator:dashboard")
    if user.is_employer:
        return redirect("employer:dashboard")
    return redirect("applicant:dashboard")


@login_required
def applicant_dashboard(request):
    if not request.user.is_applicant:
        return redirect("dashboard")
    from apps.opportunities.models import Application
    applications = request.user.applications.select_related("opportunity__company").order_by("-applied_at")
    favorites = applications.filter(is_favorite=True)
    contacts = request.user.contacts.all()[:6]
    return render(request, "accounts/applicant_dashboard.html", {
        "applications": applications,
        "favorites": favorites,
        "contacts": contacts,
    })


@login_required
def applicant_profile_edit(request):
    if not request.user.is_applicant:
        return redirect("dashboard")
    form = ApplicantProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Профиль сохранён.")
        return redirect("applicant:dashboard")
    return render(request, "accounts/profile_edit.html", {"form": form})


def public_profile_view(request, pk):
    profile_user = get_object_or_404(User, pk=pk, role=User.ROLE_APPLICANT)
    # Check privacy
    if not profile_user.profile_public and (
        not request.user.is_authenticated or
        (request.user != profile_user and not request.user.is_curator)
    ):
        messages.warning(request, "Этот профиль скрыт пользователем.")
        return redirect("home")
    is_contact = (
        request.user.is_authenticated and
        request.user != profile_user and
        profile_user in request.user.contacts.all()
    )
    pending = (
        request.user.is_authenticated and
        profile_user in request.user.contact_requests.all()
    )
    return render(request, "accounts/public_profile.html", {
        "profile_user": profile_user,
        "is_contact": is_contact,
        "pending": pending,
    })


@login_required
@require_POST
def send_contact_request(request, pk):
    target = get_object_or_404(User, pk=pk)
    if target == request.user:
        return JsonResponse({"ok": False, "msg": "Нельзя добавить себя"})
    if target in request.user.contacts.all():
        return JsonResponse({"ok": False, "msg": "Уже в контактах"})
    # If target already sent request to me — accept
    if request.user in target.contact_requests.all():
        request.user.contacts.add(target)
        target.contact_requests.remove(request.user)
        return JsonResponse({"ok": True, "msg": "Контакт добавлен"})
    request.user.contact_requests.add(target)
    return JsonResponse({"ok": True, "msg": "Заявка отправлена"})


@login_required
@require_POST
def accept_contact(request, pk):
    sender = get_object_or_404(User, pk=pk)
    if sender in request.user.pending_requests.all():
        request.user.contacts.add(sender)
        sender.contact_requests.remove(request.user)
        messages.success(request, f"{sender.display_name} добавлен в контакты.")
    return redirect("applicant:dashboard")


@login_required
def applicants_catalog(request):
    """Каталог соискателей для нетворкинга."""
    from django.db.models import Q
    qs = User.objects.filter(
        role=User.ROLE_APPLICANT,
        is_active=True,
        profile_public=True,
    ).exclude(pk=request.user.pk)

    q = request.GET.get('q', '').strip()
    skill = request.GET.get('skill', '').strip()
    university = request.GET.get('university', '').strip()

    if q:
        qs = qs.filter(
            Q(display_name__icontains=q) |
            Q(skills__icontains=q) |
            Q(bio__icontains=q)
        )
    if skill:
        qs = qs.filter(skills__icontains=skill)
    if university:
        qs = qs.filter(university__icontains=university)

    qs = qs.order_by('-date_joined')

    my_contacts = set(request.user.contacts.values_list('pk', flat=True)) if request.user.is_applicant else set()
    pending_sent = set(request.user.contact_requests.values_list('pk', flat=True)) if request.user.is_applicant else set()

    return render(request, 'accounts/catalog.html', {
        'profiles': qs,
        'q': q,
        'skill': skill,
        'university': university,
        'my_contacts': my_contacts,
        'pending_sent': pending_sent,
    })
