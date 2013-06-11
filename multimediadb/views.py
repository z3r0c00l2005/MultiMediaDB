from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth import logout
from filetransfers.api import prepare_upload, serve_file

import datetime
from multimediadb.models import Aircrafttype, Aircraftsystem, Systemgraphic, Graphicworkdone, Comments, Uploads, QA
from multimediadb.forms import TypeAddForm, SystemAddForm, SystemEditForm, GraphicAddForm, GraphicEditForm, WorkAddForm, WorkEditForm, CommentAddForm, CommentEditForm, UploadForm

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
    inqa = Systemgraphic.objects.filter(aircraftsystem_id=system_id, status__in=['Development Completed','TechnicalReview','EditorialReview','InternalQA','UploadedToLCMS','ExternalReview'])
    complete = Systemgraphic.objects.filter(aircraftsystem_id=system_id).filter(status__in=['Locked'])
    # Header Calculations
    adjest = Systemgraphic.objects.filter(aircraftsystem_id=system_id).aggregate(adjustedestimate=Sum('adjusted_hours'))
    est = Systemgraphic.objects.filter(aircraftsystem_id=system_id).aggregate(estimate=Sum('estimated_hours'))
    booked = Graphicworkdone.objects.filter(systemgraphic_id__in=allgraphics).aggregate(booked=Sum('hours_expended'))
    # Tables of comments
    comments = Comments.objects.filter(source='system', source_id=system_id,)
    uploads = Uploads.objects.filter(source='system', source_id=system_id,)
    return render(request, 'aircraftsystems/view.html', {'aircrafttype': type, 'system': system, 'allgraphics': allgraphics, 'graphics': graphics, 'holdgraphics': holdgraphics, 'inqa': inqa, 'completed': complete, 'adjest': adjest, 'est': est, 'booked': booked, 'comments': comments, 'uploads': uploads,})
    
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
    comments = Comments.objects.filter(source='graphic', source_id=graphic_id,)
    uploads = Uploads.objects.filter(source='graphic', source_id=graphic_id,)
    return render(request, 'systemgraphics/view.html', {'aircrafttype': type, 'system': system, 'graphic': graphic, 'works': works, 'comments': comments, 'uploads': uploads,})

def graphicdone(request, type_id, system_id, graphic_id):
    type = Aircrafttype.objects.get(pk=type_id)
    system = Aircraftsystem.objects.get(pk=system_id)
    graphic = Systemgraphic.objects.get(pk=graphic_id)
    Systemgraphic.objects.filter(id=graphic_id).update(status='Development Completed',)
    works = Graphicworkdone.objects.filter(systemgraphic_id=graphic_id)
    return redirect('systemview', type_id=type.id, system_id=system.id,)

def graphicholdtoggle(request, type_id, system_id, graphic_id):
    type = Aircrafttype.objects.get(pk=type_id)
    system = Aircraftsystem.objects.get(pk=system_id)
    graphic = Systemgraphic.objects.get(pk=graphic_id)
    if graphic.on_hold:
        Systemgraphic.objects.filter(id=graphic_id).update(on_hold=0,)
    else:
        Systemgraphic.objects.filter(id=graphic_id).update(on_hold=1,)
    works = Graphicworkdone.objects.filter(systemgraphic_id=graphic_id)
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
    
    
# ################
# Comment Views  #
# ################
    
def commentadd(request, type_id, system_id, graphic_id=0, graphic_version=0, source='a', commenttype='a'):
    if source == 'system':
        if 'cancel' in request.POST:
                return HttpResponseRedirect(reverse('systemview', args=(type_id, system_id))) 
        if request.method == 'POST':
            form = CommentAddForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                type = Aircrafttype.objects.get(id=type_id)
                system = Aircraftsystem.objects.get(id=system_id)
                query = Comments(source=source, source_id=system_id, comment=cd['comment'], created_by=cd['user'], comment_type='system',)
                query.save()
                return HttpResponseRedirect(reverse('systemview', args=(type_id, system_id)))    
        else:
            form = CommentAddForm()
        return render(request, 'comments/add.html', {'form': form})
    elif commenttype == 'Development':
        if 'cancel' in request.POST:
                return HttpResponseRedirect(reverse('graphicview', args=(type_id, system_id, graphic_id)))
        if request.method == 'POST':
            form = CommentAddForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                type = Aircrafttype.objects.get(id=type_id)
                system = Aircraftsystem.objects.get(id=system_id)
                graphic = Systemgraphic.objects.get(id=graphic_id)
                query = Comments(source=source, source_id=graphic_id, comment=cd['comment'], created_by=cd['user'], comment_type=commenttype, comment_version=graphic_version,)
                query.save()
                return HttpResponseRedirect(reverse('graphicview', args=(type_id, system_id, graphic_id)))    
        else:
            form = CommentAddForm()
        return render(request, 'comments/add.html', {'form': form})    
    else:
        if 'cancel' in request.POST:
                return HttpResponseRedirect(reverse('qaview', args=(type_id, system_id, graphic_id)))
        if request.method == 'POST':
            form = CommentAddForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                type = Aircrafttype.objects.get(id=type_id)
                system = Aircraftsystem.objects.get(id=system_id)
                graphic = Systemgraphic.objects.get(id=graphic_id)
                query = Comments(source=source, source_id=graphic_id, comment=cd['comment'], created_by=cd['user'], comment_type=commenttype, comment_version=graphic_version,)
                query.save()
                return HttpResponseRedirect(reverse('qaview', args=(type_id, system_id, graphic_id)))    
        else:
            form = CommentAddForm()
        return render(request, 'comments/add.html', {'form': form})    

# ################
# Upload Views   #
# ################
        
    
def upload(request, type_id, system_id, graphic_id=0, source='a'):
    if source == 'system':
        view_url = reverse('systemview', args=(type_id, system_id))
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('systemview', args=(type_id, system_id)))
        # Handle file upload
        if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                type = Aircrafttype.objects.get(id=type_id)
                system = Aircraftsystem.objects.get(id=system_id)
                newdoc = Uploads(file = request.FILES['filename'], description=cd['description'], source=source, source_id=system_id )
                newdoc.save()
                # Redirect to the document list after POST
                return HttpResponseRedirect(reverse('systemview', args=(type_id, system_id)))
        else:
            form = UploadForm() # A empty, unbound form
        return render(request, 'uploads/add.html', {'form': form})
    else:
        view_url = reverse('graphicview', args=(type_id, system_id, graphic_id))
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('graphicview', args=(type_id, system_id, graphic_id)))
        # Handle file upload
        if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                type = Aircrafttype.objects.get(id=type_id)
                system = Aircraftsystem.objects.get(id=system_id)
                newdoc = Uploads(file = request.FILES['filename'], description=cd['description'], source=source, source_id=graphic_id )
                newdoc.save()
                # Redirect to the document list after POST
                return HttpResponseRedirect(reverse('graphicview', args=(type_id, system_id, graphic_id)))
        else:
            form = UploadForm() # A empty, unbound form
        return render(request, 'uploads/add.html', {'form': form})
    

def download_handler(request, pk):
    upload = get_object_or_404(Uploads, pk=pk)
    return serve_file(request, upload.file)    
    
    
# ################
# QA Views       #
# ################    
    
def qaview(request, type_id, system_id, graphic_id):
    type = Aircrafttype.objects.get(pk=type_id)
    system = Aircraftsystem.objects.get(pk=system_id)
    graphic = Systemgraphic.objects.get(pk=graphic_id)
    comments = Comments.objects.filter(source='graphic', source_id=graphic_id,)
    uploads = Uploads.objects.filter(source='graphic', source_id=graphic_id,)
    qa = QA.objects.filter(systemgraphic=graphic.id, qa_version=graphic.version).order_by('id').reverse()[:1]

    if qa.count() == 0:
        row = QA(systemgraphic=graphic, qa_version=graphic.version,qa_stage='TechnicalReview' )
        row.save()
        Systemgraphic.objects.filter(id=graphic_id).update(status='TechnicalReview',)
        qa2 = qa.get()
    else:
        qa2 = qa.get()
    
    if qa2.qa_stage == 'TechnicalReview' and qa2.result == 'Pass':
        row = QA(systemgraphic=graphic, qa_version=graphic.version,qa_stage='EditorialReview' )
        row.save()
        Systemgraphic.objects.filter(id=graphic_id).update(status='EditorialReview',)
        
        
    if qa2.qa_stage == 'EditorialReview' and qa2.result == 'Pass':
        row = QA(systemgraphic=graphic, qa_version=graphic.version,qa_stage='InternalQA' )
        row.save()
        Systemgraphic.objects.filter(id=graphic_id).update(status='InternalQA',)
        
        
    if qa2.qa_stage == 'InternalQA' and qa2.result == 'Pass':
        row = QA(systemgraphic=graphic, qa_version=graphic.version,qa_stage='UploadedToLCMS' )
        row.save()
        Systemgraphic.objects.filter(id=graphic_id).update(status='UploadedToLCMS',)
        
    if qa2.qa_stage == 'UploadedToLCMS' and qa2.result == 'Pass':
        Systemgraphic.objects.filter(id=graphic_id).update(status='ExternalReview',)
        
    if qa2.result == 'Fail':
        row = QA(systemgraphic=graphic, qa_version=graphic.version,qa_stage='TechnicalReview' )
        row.save()
        Systemgraphic.objects.filter(id=graphic_id).update(status='TechnicalReview',)    

    qas = QA.objects.filter(systemgraphic=graphic.id).order_by('id')
    return render(request, 'qa/view.html', {'aircrafttype': type, 'system': system, 'graphic': graphic, 'qas': qas, 'comments': comments, 'uploads': uploads,})


def qaresult(request, type_id, system_id, graphic_id, graphic_version, stage, qa_id, result):
    type = Aircrafttype.objects.get(pk=type_id)
    system = Aircraftsystem.objects.get(pk=system_id)
    graphic = Systemgraphic.objects.get(pk=graphic_id)
    
    if result == 'Pass':
        if stage == 'UploadedToLCMS':
            Systemgraphic.objects.filter(id=graphic_id).update(version = int(graphic_version) + 1,)
            row = QA(systemgraphic=graphic, qa_version=graphic.version + 1,qa_stage='ExternalReview' )
            row.save()
        if stage == 'ExternalReview':
            Systemgraphic.objects.filter(id=graphic_id).update(status='Locked',)
            QA.objects.filter(pk=qa_id).update(result=result, created_by='TEST')
            return redirect('systemview', type_id=type.id, system_id=system.id)
        QA.objects.filter(pk=qa_id).update(result=result, created_by='TEST')
    else:
        QA.objects.filter(pk=qa_id).update(result=result, created_by='TEST')
        Systemgraphic.objects.filter(id=graphic_id).update(status='In Progress',)
        return redirect('systemview', type_id=type.id, system_id=system.id)
    
    return redirect('qaview', type_id=type.id, system_id=system.id, graphic_id=graphic.id)
    
    
# ################
# User Views     #
# ################      
    
def logout_view(request):
    logout(request)    
    return redirect('login')
    
    
    
    
    
    
    
    
    
