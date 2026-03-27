from django import forms
from .models import Company


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "description", "industry", "website", "linkedin",
                  "telegram", "hh_url", "city", "corporate_email", "inn"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "industry": forms.Select(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://company.com"}),
            "linkedin": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://linkedin.com/company/..."}),
            "telegram": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://t.me/company"}),
            "hh_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://hh.kz/employer/..."}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "Алматы"}),
            "corporate_email": forms.EmailInput(attrs={"class": "form-control"}),
            "inn": forms.TextInput(attrs={"class": "form-control"}),
        }
