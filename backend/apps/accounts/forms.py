from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com", "autofocus": True}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "••••••••"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Allow login by email
        self.fields["username"].widget.attrs["autocomplete"] = "email"


class RegisterApplicantForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Минимум 8 символов"}),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Повторите пароль"}),
    )

    class Meta:
        model = User
        fields = ["email", "display_name", "password1", "password2"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
            "display_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше имя"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError({"password2": "Пароли не совпадают."})
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        user.role = User.ROLE_APPLICANT
        if commit:
            user.save()
        return user


class RegisterEmployerForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Минимум 8 символов"}),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Повторите пароль"}),
    )
    company_name = forms.CharField(
        label="Название компании",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "ООО «Технологии будущего»"}),
    )
    corporate_email = forms.EmailField(
        label="Корпоративная почта",
        help_text="Подтверждает принадлежность к компании",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "hr@company.com"}),
    )
    inn = forms.CharField(
        label="ИНН / БИН",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Необязательно"}),
    )

    class Meta:
        model = User
        fields = ["email", "display_name", "password1", "password2"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "personal@example.com"}),
            "display_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "HR-менеджер / Рекрутер"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError({"password2": "Пароли не совпадают."})
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        user.role = User.ROLE_EMPLOYER
        if commit:
            user.save()
        return user


class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "display_name", "full_name", "university", "graduation_year",
            "bio", "skills", "experience", "github_url", "portfolio_url",
            "resume_url", "profile_public", "hide_applications",
        ]
        widgets = {
            "display_name": forms.TextInput(attrs={"class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "university": forms.TextInput(attrs={"class": "form-control"}),
            "graduation_year": forms.NumberInput(attrs={"class": "form-control", "min": 2020, "max": 2035}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "skills": forms.TextInput(attrs={"class": "form-control", "placeholder": "Python, Django, PostgreSQL, Git"}),
            "experience": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "github_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://github.com/username"}),
            "portfolio_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://myportfolio.com"}),
            "resume_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "Ссылка на резюме (HH, PDF...)"}),
            "profile_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "hide_applications": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
