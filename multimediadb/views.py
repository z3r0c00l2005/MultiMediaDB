from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.db.models import Sum
from django.contrib import messages
import datetime
from multimediadb.models import Aircrafttype, Aircraftsystem, Systemgraphic, Graphicworkdone
from multimediadb.forms import TypeAddForm, SystemAddForm, SystemEditForm, GraphicAddForm, GraphicEditForm, WorkAddForm, WorkEditForm
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
    # Tables of graphics
    allgraphics = Systemgraphic.objects.filter(aircraftsystem_id=system_id)
    holdgraphics = Systemgraphic.objects.filter(aircraftsystem_id=system_id).filter(status__in=['Not Started','In Progress']).filter(on_hold=1)
    graphics = Systemgraphic.objects.filter(aircraftsystem_id=system_id).filter(status__in=['Not Started','In Progress'])
    inqa = Systemgraphic.objects.filter(aircraftsystem_id=system_id, status__in=['Development Completed','Tech Review Pass','Edit Review Pass','Internal QA Pass','Uploaded LCMS'])
    complete = Systemgraphic.objects.filter(aircraftsystem_id=system_id).filter(status__in=['External Review Pass'])
    # Header Calculations
    adjest = Systemgraphic.objects.filter(aircraftsystem_id=system_id).aggregate(adjustedestimate=Sum('adjusted_hours'))
    est = Systemgraphic.objects.filter(aircraftsystem_id=system_id).aggregate(estimate=Sum('estimated_hours'))
    booked = Graphicworkdone.objects.filter(systemgraphic_id__in=allgraphics).aggregate(booked=Sum('hours_expended'))
    return render(request, 'aircraftsystems/view.html', {'aircrafttype': type, 'system': system, 'allgraphics': allgraphics, 'graphics': graphics, 'holdgraphics': holdgraphics, 'inqa': inqa, 'completed': complete, 'adjest': adjest, 'est': est, 'booked': booked,})
    
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

def graphicview(request, type_id, system_id, graphic_id):
    type = Aircrafttype.objects.get(pk=type_id)
    system = Aircraftsystem.objects.get(pk=system_id)
    graphic = Systemgraphic.objects.get(pk=graphic_id)
    works = Graphicworkdone.objects.filter(systemgraphic_id=graphic_id)
    return render(request, 'systemgraphics/view.html', {'aircrafttype': type, 'system': system, 'graphic': graphic, 'works': works,})

def graphicdone(request, type_id, system_id, graphic_id):
    type = Aircrafttype.objects.get(pk=type_id)
    system = Aircraftsystem.objects.get(pk=system_id)
    graphic = Systemgraphic.objects.get(pk=graphic_id)
    Systemgraphic.objects.filter(id=graphic_id).update(status='Development Completed',)
    works = Graphicworkdone.objects.filter(systemgraphic_id=graphic_id)
#    return render(request, 'systemgraphics/view.html', {'aircrafttype': type, 'system': system, 'graphic': graphic, 'works': works,})
    return redirect('systemview', type_id=type.id, system_id=system.id,)


# ################
# Work Views     #
# ################
    
def workadd(request, type_id, system_id, graphic_id):
    if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('graphicview', args=(type_id, system_id, graphic_id)))    
    if request.method == 'POST':
        form = WorkAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            type = Aircrafttype.objects.get(id=type_id)
            system = Aircraftsystem.objects.get(id=system_id)
            graphic = Systemgraphic.objects.get(id=graphic_id)
            query = Graphicworkdone(systemgraphic=graphic, work_carried_out=cd['work_carried_out'], created_by=cd['user'], hours_expended=cd['hours_expended'],)
            query.save()
            Systemgraphic.objects.filter(id=graphic_id).update(status='In Progress',)
            return HttpResponseRedirect(reverse('graphicview', args=(type_id, system_id, graphic_id)))    
    else:
        form = WorkAddForm()
    return render(request, 'graphicwork/add.html', {'form': form})
    
def workedit(request, type_id, system_id, graphic_id, work_id):
    if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('graphicview', args=(type_id, system_id, graphic_id)))    
    if request.method == 'POST':
        form = WorkEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            type = Aircrafttype.objects.get(id=type_id)
            system = Aircraftsystem.objects.get(id=system_id)
            graphic = Systemgraphic.objects.get(id=graphic_id)
            Graphicworkdone.objects.filter(id=work_id).update(systemgraphic=graphic, work_carried_out=cd['work_carried_out'], modified_by=cd['user'], hours_expended=cd['hours_expended'],)
            return HttpResponseRedirect(reverse('graphicview', args=(type_id, system_id, graphic_id)))    
    else:
        work = Graphicworkdone.objects.get(id=work_id)
        dictionary = model_to_dict(work, fields=[], exclude=[])
        form = WorkEditForm(initial=dictionary)
    return render(request, 'graphicwork/edit.html', {'form': form})
