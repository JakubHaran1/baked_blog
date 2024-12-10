from django import forms


class contactForm(forms.Form):
    email = forms.EmailField(label="Twój email",)
    subject = forms.CharField(label="Temat:")
    content = forms.CharField(label="Treść:", widget=forms.Textarea(attrs={
        "placeholder": 'Wpisz tu tekst'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
