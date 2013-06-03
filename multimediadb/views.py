from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.forms.models import model_to_dict
import datetime
from multimediadb.models import Aircrafttype, Aircraftsystem, Systemgraphic
from multimediadb.forms import TypeAddForm, SystemAddForm, SystemEditForm, GraphicAddForm, GraphicEditForm
# ################
# Type Views     #
# ################
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

# ################
# System Views   #
# ################
	
def systemadd(request, type_id):
    if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('typeview', args=(type_id,)))    
    if request.method == 'POST':
        form = SystemAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            type = Aircrafttype.objects.get(id=type_id)
            query = Aircraftsystem(aircrafttype=type, name=cd['name'], description=cd['description'], workshare=cd['workshare'],)
            query.save()
            return HttpResponseRedirect(reverse('typeview', args=(type_id,)))
    else:
        form = SystemAddForm()
    return render(request, 'aircraftsystems/add.html', {'form': form})

def systemedit(request, type_id, system_id):
    if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('typeview', args=(type_id,)))   
    if request.method == 'POST':
        form = SystemEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            type = Aircrafttype.objects.get(id=type_id)
            Aircraftsystem.objects.filter(id=system_id).update(aircrafttype=type, name=cd['name'], description=cd['description'], workshare=cd['workshare'],)
            return HttpResponseRedirect(reverse('typeview', args=(type_id,)))
    else:
        system = Aircraftsystem.objects.get(id=system_id)
        dictionary = model_to_dict(system, fields=[], exclude=[])
        form = SystemEditForm(initial=dictionary)
    return render(request, 'aircraftsystems/edit.html', {'form': form})

	
def systemview(request, type_id, system_id):
    type = Aircrafttype.objects.get(pk=type_id)
    system = Aircraftsystem.objects.get(pk=system_id)
    graphics = Systemgraphic.objects.filter(aircraftsystem_id=system_id)
    return render(request, 'aircraftsystems/view.html', {'aircrafttype': type, 'system': system, 'graphics': graphics,})
    
# ################
# Graphic Views  #
# ################
    
def graphicadd(request, type_id, system_id):
    if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('systemview', args=(type_id, system_id)))    
    if request.method == 'POST':
        form = GraphicAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            type = Aircrafttype.objects.get(id=type_id)
            system = Aircraftsystem.objects.get(id=system_id)
            query = Systemgraphic(aircraftsystem=system, media_label=cd['media_label'], title=cd['title'], description=cd['description'], estimated_hours=cd['estimated_hours'], adjusted_hours=cd['estimated_hours'],)
            query.save()
            return HttpResponseRedirect(reverse('systemview', args=(type_id, system_id)))
    else:
        form = GraphicAddForm()
    return render(request, 'systemgraphics/add.html', {'form': form})
    
def graphicedit(request, type_id, system_id, graphic_id):
    if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('systemview', args=(type_id, system_id)))    
    if request.method == 'POST':
        form = GraphicEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            type = Aircrafttype.objects.get(id=type_id)
            system = Aircraftsystem.objects.get(id=system_id)
            Systemgraphic.objects.filter(id=graphic_id).update(aircraftsystem=system, media_label=cd['media_label'], title=cd['title'], description=cd['description'], adjusted_hours=cd['adjusted_hours'],)
            return HttpResponseRedirect(reverse('systemview', args=(type_id, system_id)))
    else:
        graphic = Systemgraphic.objects.get(id=graphic_id)
        dictionary = model_to_dict(graphic, fields=[], exclude=[])
        form = GraphicEditForm(initial=dictionary)
    return render(request, 'systemgraphics/edit.html', {'form': form})