from django.http import JsonResponse
from django.views.generic import TemplateView
from apps.opportunities.models import Opportunity, Tag


class HomeView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tags"] = Tag.objects.filter(tag_type=Tag.TAG_TYPE_SKILL)[:20]
        ctx["type_choices"] = Opportunity.TYPE_CHOICES
        ctx["format_choices"] = Opportunity.FORMAT_CHOICES
        ctx["total_opps"] = Opportunity.objects.filter(
            status=Opportunity.STATUS_ACTIVE, is_moderated=True
        ).count()
        ctx["recent_opps"] = Opportunity.objects.filter(
            status=Opportunity.STATUS_ACTIVE, is_moderated=True
        ).select_related("company").prefetch_related("tags").order_by("-published_at")[:8]
        return ctx


def healthcheck(request):
    return JsonResponse({"status": "ok", "service": "tramplin-ada"})
