from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from .models import Opportunity, Tag, Application
from .forms import OpportunityForm, ApplicationForm


def opportunity_list(request):
    qs = Opportunity.objects.filter(
        status=Opportunity.STATUS_ACTIVE,
        is_moderated=True,
    ).select_related("company").prefetch_related("tags")

    # Filters
    q = request.GET.get("q", "").strip()
    opp_type = request.GET.get("opp_type", "")
    work_format = request.GET.get("work_format", "")
    tag_ids = request.GET.getlist("tags")
    salary_min = request.GET.get("salary_min", "")
    city = request.GET.get("city", "").strip()

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(company__name__icontains=q))
    if opp_type:
        qs = qs.filter(opp_type=opp_type)
    if work_format:
        qs = qs.filter(work_format=work_format)
    if tag_ids:
        qs = qs.filter(tags__id__in=tag_ids).distinct()
    if salary_min:
        try:
            qs = qs.filter(salary_min__gte=int(salary_min))
        except ValueError:
            pass
    if city:
        qs = qs.filter(Q(city__icontains=city) | Q(address__icontains=city))

    paginator = Paginator(qs, 12)
    page = request.GET.get("page", 1)
    opportunities = paginator.get_page(page)

    tags = Tag.objects.all()
    return render(request, "opportunities/list.html", {
        "opportunities": opportunities,
        "tags": tags,
        "q": q,
        "opp_type": opp_type,
        "work_format": work_format,
        "selected_tags": [int(t) for t in tag_ids if t.isdigit()],
        "salary_min": salary_min,
        "city": city,
        "type_choices": Opportunity.TYPE_CHOICES,
        "format_choices": Opportunity.FORMAT_CHOICES,
    })


def opportunity_detail(request, pk):
    opp = get_object_or_404(Opportunity, pk=pk, status=Opportunity.STATUS_ACTIVE, is_moderated=True)
    user_applied = False
    user_application = None
    if request.user.is_authenticated and request.user.is_applicant:
        try:
            user_application = Application.objects.get(applicant=request.user, opportunity=opp)
            user_applied = True
        except Application.DoesNotExist:
            pass

    form = ApplicationForm()
    similar = Opportunity.objects.filter(
        status=Opportunity.STATUS_ACTIVE,
        is_moderated=True,
        opp_type=opp.opp_type,
    ).exclude(pk=opp.pk).select_related("company")[:4]

    return render(request, "opportunities/detail.html", {
        "opp": opp,
        "form": form,
        "user_applied": user_applied,
        "user_application": user_application,
        "similar": similar,
    })


@login_required
@require_POST
def apply_opportunity(request, pk):
    if not request.user.is_applicant:
        messages.error(request, "Только соискатели могут откликаться на вакансии.")
        return redirect("opportunity_detail", pk=pk)
    opp = get_object_or_404(Opportunity, pk=pk, status=Opportunity.STATUS_ACTIVE)
    if Application.objects.filter(applicant=request.user, opportunity=opp).exists():
        messages.warning(request, "Вы уже откликались на эту вакансию.")
        return redirect("opportunity_detail", pk=pk)
    form = ApplicationForm(request.POST)
    if form.is_valid():
        Application.objects.create(
            applicant=request.user,
            opportunity=opp,
            cover_letter=form.cleaned_data.get("cover_letter", ""),
        )
        messages.success(request, "Отклик отправлен! Ждите ответа от работодателя.")
    return redirect("opportunity_detail", pk=pk)


@login_required
@require_POST
def toggle_favorite(request, pk):
    opp = get_object_or_404(Opportunity, pk=pk)
    if not request.user.is_applicant:
        return JsonResponse({"ok": False})
    app, created = Application.objects.get_or_create(
        applicant=request.user,
        opportunity=opp,
        defaults={"is_favorite": True, "cover_letter": ""},
    )
    if not created:
        app.is_favorite = not app.is_favorite
        app.save(update_fields=["is_favorite"])
    return JsonResponse({"ok": True, "is_favorite": app.is_favorite})


# ---- Employer views ----

@login_required
def employer_dashboard(request):
    if not request.user.is_employer:
        return redirect("dashboard")
    try:
        company = request.user.company
    except Exception:
        messages.error(request, "Компания не найдена.")
        return redirect("home")

    status_filter = request.GET.get("status", "")
    opps = company.opportunities.prefetch_related("tags")
    if status_filter:
        opps = opps.filter(status=status_filter)
    opps = opps.order_by("-published_at")

    return render(request, "opportunities/employer_dashboard.html", {
        "company": company,
        "opportunities": opps,
        "status_filter": status_filter,
        "status_choices": Opportunity.STATUS_CHOICES,
        "total_applications": Application.objects.filter(opportunity__company=company).count(),
    })


@login_required
def opportunity_create(request):
    if not request.user.is_employer:
        return redirect("dashboard")
    try:
        company = request.user.company
    except Exception:
        messages.error(request, "Сначала создайте компанию.")
        return redirect("dashboard")
    if not company.is_verified:
        messages.warning(request, "Создание вакансий доступно только после верификации компании.")
        return redirect("employer:dashboard")

    form = OpportunityForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        opp = form.save(commit=False)
        opp.company = company
        opp.save()
        form.save_m2m()
        messages.success(request, "Вакансия создана и отправлена на модерацию.")
        return redirect("employer:dashboard")
    tags_by_type = {
        "skill": Tag.objects.filter(tag_type=Tag.TAG_TYPE_SKILL),
        "level": Tag.objects.filter(tag_type=Tag.TAG_TYPE_LEVEL),
        "employment": Tag.objects.filter(tag_type=Tag.TAG_TYPE_EMPLOYMENT),
    }
    return render(request, "opportunities/opportunity_form.html", {
        "form": form, "tags_by_type": tags_by_type, "action": "Создать",
    })


@login_required
def opportunity_edit(request, pk):
    if not request.user.is_employer:
        return redirect("dashboard")
    opp = get_object_or_404(Opportunity, pk=pk, company=request.user.company)
    form = OpportunityForm(request.POST or None, instance=opp)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Вакансия обновлена.")
        return redirect("employer:dashboard")
    tags_by_type = {
        "skill": Tag.objects.filter(tag_type=Tag.TAG_TYPE_SKILL),
        "level": Tag.objects.filter(tag_type=Tag.TAG_TYPE_LEVEL),
        "employment": Tag.objects.filter(tag_type=Tag.TAG_TYPE_EMPLOYMENT),
    }
    return render(request, "opportunities/opportunity_form.html", {
        "form": form, "tags_by_type": tags_by_type, "action": "Сохранить", "opp": opp,
    })


@login_required
def employer_applicants(request, pk):
    if not request.user.is_employer:
        return redirect("dashboard")
    opp = get_object_or_404(Opportunity, pk=pk, company=request.user.company)
    applications = opp.applications.select_related("applicant").order_by("-applied_at")
    return render(request, "opportunities/applicants.html", {
        "opp": opp,
        "applications": applications,
        "status_choices": Application.STATUS_CHOICES,
    })


@login_required
@require_POST
def update_application_status(request, app_id):
    if not request.user.is_employer:
        return redirect("dashboard")
    app = get_object_or_404(Application, pk=app_id, opportunity__company=request.user.company)
    new_status = request.POST.get("status")
    if new_status in dict(Application.STATUS_CHOICES):
        app.status = new_status
        app.save(update_fields=["status"])
    return redirect("employer:applicants", pk=app.opportunity_id)


@login_required
def employer_company_edit(request):
    if not request.user.is_employer:
        return redirect("dashboard")
    from apps.companies.forms import CompanyProfileForm
    try:
        company = request.user.company
    except Exception:
        messages.error(request, "Компания не найдена.")
        return redirect("dashboard")
    form = CompanyProfileForm(request.POST or None, instance=company)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Данные компании обновлены.")
        return redirect("employer:dashboard")
    return render(request, "opportunities/company_edit.html", {"form": form, "company": company})


# ---- API for map ----

def api_map_markers(request):
    qs = Opportunity.objects.filter(
        status=Opportunity.STATUS_ACTIVE,
        is_moderated=True,
    ).exclude(latitude=None).select_related("company")

    # Apply same filters as list
    opp_type = request.GET.get("opp_type", "")
    work_format = request.GET.get("work_format", "")
    if opp_type:
        qs = qs.filter(opp_type=opp_type)
    if work_format:
        qs = qs.filter(work_format=work_format)

    data = []
    for opp in qs:
        data.append({
            "id": opp.pk,
            "title": opp.title,
            "company": opp.company.name,
            "opp_type": opp.opp_type,
            "opp_type_display": opp.get_opp_type_display(),
            "work_format": opp.work_format,
            "salary": opp.salary_display,
            "city": opp.city,
            "lat": float(opp.latitude),
            "lng": float(opp.longitude),
            "url": f"/opportunities/{opp.pk}/",
            "tags": [t.name for t in opp.tags.all()[:4]],
        })
    return JsonResponse({"markers": data})
