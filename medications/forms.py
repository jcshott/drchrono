from django import forms
CHOICES = (("approve", "Auto-approve renewal"), ("contact", "Contact patient for appointment"))

class RenewalForm(forms.Form):
    action = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    med_id = forms.CharField(widget=forms.widgets.HiddenInput())
    renew_amt = forms.CharField(widget=forms.widgets.HiddenInput(), initial=0)
