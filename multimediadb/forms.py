from django import forms

class TypeAddForm(forms.Form):
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=50)
    
class SystemAddForm(forms.Form):
    WORKSHARE_CHOICES = (
        ('UK', 'UK'),
        ('IT', 'Italy'),
    )

    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=50)
    workshare = forms.ChoiceField(choices=WORKSHARE_CHOICES)