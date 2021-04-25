
from django import forms
from django.forms.widgets import NumberInput

class DateForm(forms.Form):
    """Form to present date-picker widget to user"""
    
    date = forms.DateField(label="Select a date", widget=NumberInput(attrs={'type': 'date'}))