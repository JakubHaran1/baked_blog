from django import forms


from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm

from .models import UserCommentModel, CustomUserModel


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


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        max_length=70, min_length=8, required=True, label="Nazwa użytkownika:",  widget=forms.TextInput(attrs={'placeholder': 'Zbyszko123'}))
    email = forms.EmailField(
        required=True, label="Email:",  widget=forms.TextInput(attrs={'placeholder': 'Zbyszko123@gmail.com'}))
    password1 = forms.CharField(
        min_length=8, required=True, widget=forms.PasswordInput, label="Podaj hasło:")
    password2 = forms.CharField(
        min_length=8, required=True, widget=forms.PasswordInput, label="Potwiedź hasło")

    class Meta():
        model = CustomUserModel
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].error_messages = {
            "unique": "Nazwa użytkownika jest już zajęta!",
            "required": "Musisz podać nazwę użytkownika",
            "min_length": "Podajesz zbyt krótką nazwę użytkownika!",
            "min_length": "Podajesz za długą nazwę użytkownika!"
        }
        self.fields["email"].error_messages = {
            "required": "Pole email jest wymagane!",
            "invalid": "Podaj poprawny email!"
        }
        self.fields["password1"].error_messages = {
            "required": "Hasło jest wymagane!",
            "min_length": "Hasło jest za krótkie!"
        }
        self.fields["password2"].error_messages = {
            "required": "Hasło jest wymagane!",
            "min_length": "Hasło jest za krótkie!"
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie są zgodne!")

        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        users = CustomUserModel.objects.filter(email=email).count()
        if users:
            raise forms.ValidationError(
                "Już istnieje użytkownik o takim adresie email!")

        return email


class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=70, required=True, label="Nazwa użytkownika:", widget=forms.TextInput(attrs={
                               "placeholder": "zbyszko123"}))
    password = forms.CharField(label="Podaj swoje hasło:",
                               widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].error_messages = {
            "invalid": "Nazwa użytkownika jest nieprawidłowa",
            "required": "Musisz podać nazwę użytkownika",
            "min_length": "Próbujesz podać zbyt krótką nazwę użytkownika!"
        }
        self.fields["password"].error_messages = {
            "invalid": "Hasło jest nieprawidłowe!",
            "required": "Musisz podać hasło!",
            "min_length": "Próbujesz podać zbyt krótkie hasło!"
        }


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = UserCommentModel
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].error_messages = {
            "required": "Musisz podać treść komentarza"
        }


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        min_length=8, required=True, widget=forms.PasswordInput, label="Podaj hasło:")
    password2 = forms.CharField(
        min_length=8, required=True, widget=forms.PasswordInput, label="Potwiedź hasło:")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].error_messages = self.fields["password2"].error_messages = {
            "invalid": "Hasło jest nieprawidłowe!",
            "required": "Musisz podać hasło!",
            "min_length": "Próbujesz podać zbyt krótkie hasło!"
        }

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Hasła nie są zgodne!")

        return password2
