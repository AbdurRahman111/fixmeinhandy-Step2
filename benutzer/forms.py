from django import forms 
from .models import Auftrag 
from django.core.validators import EmailValidator, RegexValidator
import re

class DateInput(forms.DateInput):
    input_type = 'date'

class KundendatenForm(forms.ModelForm):
    class Meta:
        model = Auftrag 
        fields = ['vorname', 
            'nachname',
            'email',
            # 'geburtsdatum',
            'telefon',
            'ort',
            'Adresszeile',
            'Hausnummer',
            'Stadt',
            'Postleitzahl']

        # widgets = {
        #     'geburtsdatum': DateInput()
        # }

    english_text_validator = RegexValidator(
        regex=r'^[a-zA-Z]*$',
        message="Only English characters are allowed.",
        # flags = re.IGNORECASE  # This flag makes the regex case-insensitive
    )

    email_validator = EmailValidator(message="Invalid email address.")

    vorname = forms.CharField(
        validators=[english_text_validator],
        required=True,
    )

    email = forms.EmailField(
        validators=[email_validator],
        required=True,
    )
