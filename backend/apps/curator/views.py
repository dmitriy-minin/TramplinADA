from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q

from apps.accounts.models import User
from apps.companies.models import Company
from apps.opportunities.models import Opportunity, Tag, Application
from apps.opportunities.forms import TagForm
from apps.companies.forms import CompanyProfileForm


def curator_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_curator:
            messages.error(request, "Доступ запрещён.")
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_curator:
            messages.error(request, "Доступ запрещён.")
            return redirect("home")
        try:
            if not request.user.curator_profile.is_admin:
                messages.error(request, "Только администратор может выполнять это действие.")
                return redirect("curator:dashboard")
        except Exception:
            messages.error(request, "Доступ запрещён.")
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper


@curator_required
def curator_dashboard(request):
    pending_companies = Company.objects.filter(status=Company.STATUS_PENDING).count()
    pending_opps = Opportunity.objects.filter(is_moderated=False, status=Opportunity.STATUS_ACTIVE).count()
    total_users = User.objects.filter(role=User.ROLE_APPLICANT).count()
    total_employers = User.objects.filter(role=User.ROLE_EMPLOYER).count()
    recent_opps = Opportunity.objects.filter(is_moderated=False).order_by("-published_at")[:5]
    recent_companies = Company.objects.filter(status=Company.STATUS_PENDING).order_by("-created_at")[:5]

    return render(request, "curator/dashboard.html", {
        "pending_companies": pending_companies,
        "pending_opps": pending_opps,
        "total_users": total_users,
        "total_employers": total_employers,
        "recent_opps": recent_opps,
        "recent_companies": recent_companies,
    })


@curator_required
def companies_list(request):
    status = request.GET.get("status", "")
    q = request.GET.get("q", "").strip()
    qs = Company.objects.select_related("owner").order_by("-created_at")
    if status:
        qs = qs.filter(status=status)
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(owner__email__icontains=q))
    return render(request, "curator/companies.html", {
        "companies": qs,
        "status": status,
        "q": q,
        "status_choices": Company.STATUS_CHOICES,
    })


@curator_required
@require_POST
def verify_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    action = request.POST.get("action")
    note = request.POST.get("note", "")
    if action == "verify":
        company.status = Company.STATUS_VERIFIED
        messages.success(request, f"Компания «{company.name}» верифицирована.")
    elif action == "reject":
        company.status = Company.STATUS_REJECTED
        messages.warning(request, f"Компания «{company.name}» отклонена.")
    company.verification_note = note
    company.save(update_fields=["status", "verification_note"])
    return redirect("curator:companies")


@curator_required
def opportunities_moderation(request):
    status = request.GET.get("status", "")
    q = request.GET.get("q", "").strip()
    qs = Opportunity.objects.select_related("company").order_by("-published_at")
    if not status:
        # Default: show pending moderation
        qs = qs.filter(is_moderated=False)
    else:
        qs = qs.filter(status=status)
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(company__name__icontains=q))
    return render(request, "curator/opportunities.html", {
        "opportunities": qs,
        "status": status,
        "q": q,
        "status_choices": Opportunity.STATUS_CHOICES,
    })


@curator_required
@require_POST
def moderate_opportunity(request, pk):
    opp = get_object_or_404(Opportunity, pk=pk)
    action = request.POST.get("action")
    note = request.POST.get("note", "")
    if action == "approve":
        opp.is_moderated = True
        opp.status = Opportunity.STATUS_ACTIVE
        messages.success(request, f"«{opp.title}» одобрена.")
    elif action == "reject":
        opp.is_moderated = False
        opp.status = Opportunity.STATUS_CLOSED
        messages.warning(request, f"«{opp.title}» отклонена.")
    opp.moderation_note = note
    opp.save(update_fields=["is_moderated", "status", "moderation_note"])
    return redirect("curator:opportunities")


@curator_required
def users_list(request):
    role = request.GET.get("role", "")
    q = request.GET.get("q", "").strip()
    qs = User.objects.exclude(role=User.ROLE_CURATOR).order_by("-date_joined")
    if role:
        qs = qs.filter(role=role)
    if q:
        qs = qs.filter(Q(email__icontains=q) | Q(display_name__icontains=q))
    return render(request, "curator/users.html", {
        "users": qs,
        "role": role,
        "q": q,
        "role_choices": [(User.ROLE_APPLICANT, "Соискатели"), (User.ROLE_EMPLOYER, "Работодатели")],
    })


@curator_required
def user_detail(request, pk):
    target = get_object_or_404(User, pk=pk)
    return render(request, "curator/user_detail.html", {"target": target})


@curator_required
@require_POST
def toggle_user_active(request, pk):
    target = get_object_or_404(User, pk=pk)
    target.is_active = not target.is_active
    target.save(update_fields=["is_active"])
    action = "активирован" if target.is_active else "заблокирован"
    messages.success(request, f"Пользователь {target.email} {action}.")
    return redirect("curator:users")


@curator_required
def tags_list(request):
    tags = Tag.objects.all().order_by("tag_type", "name")
    form = TagForm()
    return render(request, "curator/tags.html", {"tags": tags, "form": form})


@curator_required
def tag_create(request):
    form = TagForm(request.POST)
    if form.is_valid():
        tag = form.save(commit=False)
        tag.created_by = request.user
        tag.save()
        messages.success(request, f"Тег «{tag.name}» создан.")
    return redirect("curator:tags")


@curator_required
@require_POST
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk, is_system=False)
    tag.delete()
    messages.success(request, "Тег удалён.")
    return redirect("curator:tags")


@admin_required
def curators_list(request):
    from apps.curator.models import CuratorProfile
    curators = User.objects.filter(role=User.ROLE_CURATOR).select_related("curator_profile")
    return render(request, "curator/curators.html", {"curators": curators})


@admin_required
def curator_create(request):
    from apps.curator.models import CuratorProfile
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        name = request.POST.get("display_name", "").strip()
        password = request.POST.get("password", "")
        university = request.POST.get("university", "")
        position = request.POST.get("position", "")
        if not email or not password:
            messages.error(request, "Email и пароль обязательны.")
            return redirect("curator:curators")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Пользователь с таким email уже существует.")
            return redirect("curator:curators")
        user = User.objects.create_user(
            username=email, email=email, password=password,
            display_name=name, role=User.ROLE_CURATOR,
        )
        CuratorProfile.objects.create(user=user, university=university, position=position)
        messages.success(request, f"Куратор {email} создан.")
        return redirect("curator:curators")
    return redirect("curator:curators")
