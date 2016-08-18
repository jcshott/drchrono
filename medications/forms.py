from django import forms
CHOICES = (("approve", "Auto-approve renewal"), ("contact", "Contact patient for appointment"))

class RenewalForm(forms.Form):
    action = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    renew_amt = forms.IntegerField(min_value=0, initial=0)
    med_id = forms.CharField(widget=forms.widgets.HiddenInput())
