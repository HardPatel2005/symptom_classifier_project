# classifier_app/forms.py

from django import forms

class SymptomForm(forms.Form):
    symptom_text = forms.CharField(
        label='Describe your symptom',
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'e.g., "I have a persistent cough and fever."'}),
        max_length=500,
        help_text="Please provide a brief description of your symptom."
    )