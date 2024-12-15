from django import forms
from .models import CustomUserModel
from django.contrib.auth import aauthenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


class contactForm(forms.Form):
    email = forms.EmailField(label="Twój email",)
    subject = forms.CharField(label="Temat:")
    content = forms.CharField(label="Treść:", widget=forms.Textarea(attrs={
        "placeholder": 'Wpisz tu tekst'
    }))

    def __init__(self):
        super().__init__()
        self.fields["email"].error_messages = {
            "required": "Pole email jest wymagane!",
            "invalid": "Podaj poprawny email!"
        }
        self.fields["subject"].error_messages = {
            "required": "Temat jest wymagany!",

        }
        self.fields["content"].error_messages = {
            "required": "Treść wiadomości jest wymagana!",

        }


class CreateUserForm(forms.ModelForm):
    password_field = forms.CharField(
        label="Hasło:", required=True, widget=forms.PasswordInput, min_length=8)
    password_field_confirm = forms.CharField(
        label="Potwiedź Hasło:", required=True, widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = CustomUserModel
        fields = ["name", "second_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].error_messages = {
            "unique": "Podany adres e-mail już istnieje w systemie!",
            "required": "Adres e-mail jest wymagany!",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_field")
        password_confirm = cleaned_data.get("password_field_confirm")

        if not password:
            self.add_error("password_field", "Hasło nie może być puste.")

        if password != password_confirm:
            self.add_error("password_field", "Hasła nie są takie same!")
            self.add_error("password_field_confirm",
                           "Hasła nie są takie same!")

        return cleaned_data

    def send_registration_email(self):
        user_email = self.cleaned_data.get("email")
        user_name = self.cleaned_data.get("name")
        send_mail(subject="Dziękuje za dołączenie do mojej grupy!",
                  message=f"Dzięki ci {user_name}:)", from_email="helenazbozycka@gmail.com", recipient_list=[f"{user_email}"])

    def save(self, commit=True):
        user_data = super().save(commit=False)
        password = self.cleaned_data.get("password_field")

        if password:
            user_data.set_password(password)

        if commit:
            user_data.save()

        return user_data
