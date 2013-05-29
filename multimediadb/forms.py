from django import forms

class TypeAddForm(forms.Form):
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=50)
    