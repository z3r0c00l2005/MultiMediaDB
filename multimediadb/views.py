from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
import datetime
from multimediadb.models import Aircrafttype, Aircraftsystem
from multimediadb.forms import TypeAddForm

def typeindex(request):
    types = Aircrafttype.objects.all()
    return render(request, 'aircrafttypes/index.html', {'types': types})
    
def typeview(request, type_id):
    type = Aircrafttype.objects.get(pk=type_id)
    systems = Aircraftsystem.objects.filter(aircrafttype_id=type_id)
    return render(request, 'aircrafttypes/view.html', {'aircrafttype': type, 'systems': systems})

def typeadd(request):
    if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('typeindex'))    
    if request.method == 'POST':
        form = TypeAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            query = Aircrafttype(name=cd['name'], description=cd['description'])
            query.save()
            return HttpResponseRedirect(reverse('typeindex'))
    else:
        form = TypeAddForm()
    return render(request, 'aircrafttypes/add.html', {'form': form})