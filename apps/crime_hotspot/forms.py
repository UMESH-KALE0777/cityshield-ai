from django import forms
from .models import CrimeReport

CRIME_CHOICES = [
    ('Theft', 'Theft'),
    ('Robbery', 'Robbery'),
    ('Assault', 'Assault'),
    ('Kidnapping', 'Kidnapping'),
    ('Murder', 'Murder'),
    ('Cheating', 'Cheating/Fraud'),
    ('Other', 'Other'),
]

class CrimeReportForm(forms.ModelForm):
    crime_type = forms.ChoiceField(
        choices=CRIME_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full border p-3 rounded'})
    )

    class Meta:
        model = CrimeReport
        fields = ['crime_type', 'date', 'time', 'location', 'description']
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'w-full border p-3 rounded', 'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'w-full border p-3 rounded', 'type': 'time'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full border p-3 rounded',
                'placeholder': 'e.g. MG Road, Bangalore'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border p-3 rounded', 'rows': 4
            }),
        }
