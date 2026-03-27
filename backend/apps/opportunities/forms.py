from django import forms
from .models import Opportunity, Tag


class OpportunityForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Теги",
    )

    class Meta:
        model = Opportunity
        fields = [
            "title", "description", "opp_type", "work_format",
            "address", "city", "latitude", "longitude",
            "salary_min", "salary_max", "salary_currency",
            "expires_at", "event_date",
            "contact_email", "contact_phone", "external_url",
            "status", "tags",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Python Backend Developer"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 8,
                                                  "placeholder": "Опишите позицию, требования к кандидату..."}),
            "opp_type": forms.Select(attrs={"class": "form-control"}),
            "work_format": forms.Select(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "ул. Пушкина, 10, офис 305"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "Алматы"}),
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "salary_min": forms.NumberInput(attrs={"class": "form-control", "placeholder": "300000"}),
            "salary_max": forms.NumberInput(attrs={"class": "form-control", "placeholder": "500000"}),
            "salary_currency": forms.Select(
                choices=[("KZT", "KZT"), ("USD", "USD"), ("RUB", "RUB")],
                attrs={"class": "form-control"},
            ),
            "expires_at": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "event_date": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "contact_email": forms.EmailInput(attrs={"class": "form-control"}),
            "contact_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+7 (777) 000-00-00"}),
            "external_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class ApplicationForm(forms.Form):
    cover_letter = forms.CharField(
        label="Сопроводительное письмо",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Расскажите, почему вы подходите для этой позиции...",
        }),
    )


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name", "tag_type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "tag_type": forms.Select(attrs={"class": "form-control"}),
        }
