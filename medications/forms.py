from django import forms
CHOICES = (("approve", "approve renewal"), ("contact", "contact patient"))

class RenewalForm(forms.Form):
    action = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    med_id = forms.CharField(widget=forms.widgets.HiddenInput())
