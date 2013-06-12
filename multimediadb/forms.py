from django import forms
from django.contrib.auth.models import User, Group

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
    
class SystemEditForm(forms.Form):
    WORKSHARE_CHOICES = (
        ('UK', 'UK'),
        ('IT', 'Italy'),
    )
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=50)
    workshare = forms.ChoiceField(choices=WORKSHARE_CHOICES)
    
class GraphicAddForm(forms.Form):
    media_label = forms.CharField(max_length=100)
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=50)
    estimated_hours = forms.DecimalField(max_digits=5, decimal_places=2)

class GraphicEditForm(forms.Form):
    media_label = forms.CharField(max_length=100)
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=50)
    adjusted_hours = forms.DecimalField(max_digits=5, decimal_places=2)

class WorkAddForm(forms.Form):
    work_carried_out = forms.CharField(widget = forms.Textarea)
    hours_expended = forms.DecimalField(max_digits=5, decimal_places=2)
    
class WorkEditForm(forms.Form):
    work_carried_out = forms.CharField(widget = forms.Textarea)
    hours_expended = forms.DecimalField(max_digits=5, decimal_places=2)
    
class CommentAddForm(forms.Form):
    comment = forms.CharField(widget = forms.Textarea)
    
class CommentEditForm(forms.Form):
    comment = forms.CharField(max_length=600)
    
class UploadForm(forms.Form):
    filename = forms.FileField(required=False)
    description = forms.CharField(max_length=50)
    
class NewLoginForm(forms.Form):
    """ 
    Form for creating new login
    """
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    groups = forms.ModelChoiceField(queryset=Group.objects.all())
    password = forms.CharField(widget=forms.PasswordInput)
    check_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        try:
            if self.cleaned_data['password'] != self.cleaned_data['check_password']:
                raise forms.ValidationError("Passwords entered do not match")
        except KeyError:
            # didn't find what we expected in data - fields are blank on front end.  Fields
            # are required by default so we don't need to worry about validation
            pass
        return self.cleaned_data
