from django import forms
CHOICES = (("approve", "approve refill"), ("contact", "contact patient"))

class RefillForm(forms.Form):
    action = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
