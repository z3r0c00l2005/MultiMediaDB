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
    work_carried_out = forms.CharField(max_length=50)
    user = forms.CharField(max_length=50)
    hours_expended = forms.DecimalField(max_digits=5, decimal_places=2)
    
class WorkEditForm(forms.Form):
    work_carried_out = forms.CharField(max_length=50)
    user = forms.CharField(max_length=50)
    hours_expended = forms.DecimalField(max_digits=5, decimal_places=2)
    
class CommentAddForm(forms.Form):
    comment = forms.CharField(max_length=600)
    user = forms.CharField(max_length=50)
    
class CommentEditForm(forms.Form):
    comment = forms.CharField(max_length=600)
    user = forms.CharField(max_length=50)
    
class UploadForm(forms.Form):
    filename = forms.FileField(required=False)
    description = forms.CharField(max_length=50)
