from django import forms


class contactForm(forms.Form):
    email = forms.EmailField(label="Twój email")
    subject = forms.CharField(label="Temat:")
    content = forms.CharField(label="Treść:", widget=forms.Textarea(attrs={
        "placeholder": 'Wpisz tu tekst'
    }))
