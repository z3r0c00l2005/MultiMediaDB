from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from filetransfers.api import prepare_upload, serve_file
from django.contrib.auth.models import User
import datetime, csv
from multimediadb.models import Aircrafttype, Aircraftsystem, Systemgraphic, Graphicworkdone, Comments, Uploads, QA, Aircraft3Dsystem, Status3D
from multimediadb.forms import TypeAddForm, TypeEditForm, SystemAddForm, SystemEditForm, GraphicAddForm, GraphicEditForm, WorkAddForm, WorkEditForm, CommentAddForm, CommentEditForm, UploadForm, NewLoginForm, PasswordChange, UserEdit, ImportForm, System3DAddForm, System3DEditForm

# ################
# Type Views     #
# ################
@login_required
def typeindex(request):
    types = Aircrafttype.objects.all()
    return render(request, 'aircrafttypes/index.html', {'types': types})

@login_required    
def typeview(request, type_id):
    type = Aircrafttype.objects.get(pk=type_id)

    is_manager = request.user.groups.filter(name='Managers').count() | request.user.is_superuser
    systems = Aircraftsystem.objects.filter(aircrafttype_id=type_id).order_by('-workshare', 'name')
    
    for system in systems:
        system.total = Systemgraphic.objects.filter(aircraftsystem_id=system.id).count()
        system.notdone = Systemgraphic.objects.filter(aircraftsystem_id=system.id).filter(status__in=['Not Started']).filter(on_hold=0).count()
        system.work = Systemgraphic.objects.filter(aircraftsystem_id=system.id).filter(status__in=['In Progress']).filter(on_hold=0).count()
        system.hold = Systemgraphic.objects.filter(aircraftsystem_id=system.id).filter(status__in=['Not Started','In Progress']).filter(on_hold=1).count()
        system.qa = Systemgraphic.objects.filter(aircraftsystem_id=system.id, status__in=['Development Completed','TechnicalReview','EditorialReview','InternalQA','UploadedToLCMS','ExternalReview']).count()
        system.complete = Systemgraphic.objects.filter(aircraftsystem_id=system.id).filter(status__in=['Locked']).count()
        # Hours
        system.adjest = Systemgraphic.objects.filter(aircraftsystem_id=system.id).aggregate(adjustedestimate=Sum('adjusted_hours'))
        allgraphics = Systemgraphic.objects.filter(aircraftsystem_id=system.id).order_by('media_label', 'version')
        system.booked = Graphicworkdone.objects.filter(systemgraphic_id__in=allgraphics).aggregate(booked=Sum('hours_expended'))
        
        if system.adjest["adjustedestimate"] is None:
            system.adjest["adjustedestimate"] = 0
        
        if system.booked["booked"] is None:
            system.booked["booked"] = 0
        system.delta = system.adjest["adjustedestimate"] - system.booked["booked"]
        
        if system.total!=0:
            onepc = 100.0/system.total
            system.notdonepc = system.notdone*onepc
            system.workpc = system.work*onepc
            system.holdpc = system.hold * onepc
            system.qapc = system.qa * onepc
            system.completepc = system.complete * onepc
  
    # assert false, locals()
    return render(request, 'aircrafttypes/view.html', {'aircrafttype': type, 'systems': systems, 'is_manager': is_manager})

@login_required
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

@login_required
def typeedit(request, type_id):
    if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('typeindex'))   
    if request.method == 'POST':
        form = TypeEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Aircrafttype.objects.filter(id=type_id).update(name=cd['name'], description=cd['description'],)
            return HttpResponseRedirect(reverse('typeindex'))
    else:
        type = Aircrafttype.objects.get(id=type_id)
        dictionary = model_to_dict(type, fields=[], exclude=[])
        form = TypeEditForm(initial=dictionary)
    return render(request, 'aircrafttypes/edit.html', {'form': form})

@login_required    
def typeview3d(request, type_id):
    type = Aircrafttype.objects.get(pk=type_id)
    systems = Aircraft3Dsystem.objects.filter(aircrafttype_id=type_id).order_by('name')

    for system in systems:
        #system.total = Systemgraphic.objects.filter(aircraftsystem_id=system.id).count()
        #system.notdone = Systemgraphic.objects.filter(aircraftsystem_id=system.id).filter(status__in=['Not Started']).filter(on_hold=0).count()
        #system.work = Systemgraphic.objects.filter(aircraftsystem_id=system.id).filter(status__in=['In Progress']).filter(on_hold=0).count()
        #system.hold = Systemgraphic.objects.filter(aircraftsystem_id=system.id).filter(status__in=['Not Started','In Progress']).filter(on_hold=1).count()
        #system.qa = Systemgraphic.objects.filter(aircraftsystem_id=system.id, status__in=['Development Completed','TechnicalReview','EditorialReview','InternalQA','UploadedToLCMS','ExternalReview']).count()
        #system.complete = Systemgraphic.objects.filter(aircraftsystem_id=system.id).filter(status__in=['Locked']).count()

        #if system.total!=0:
        #    onepc = 100.0/system.total
        #    system.notdonepc = system.notdone*onepc
        #    system.workpc = system.work*onepc
        #    system.holdpc = system.hold * onepc
        #    system.qapc = system.qa * onepc
        #    system.completepc = system.complete * onepc
        a = 1
    # assert false, locals()
    return render(request, 'aircrafttypes/view3d.html', {'aircrafttype': type, 'systems': systems})

# ################
# System Views   #
# ################
	
@login_required
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

@login_required
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

@login_required
def systemview(request, type_id, system_id):
    type = Aircrafttype.objects.get(pk=type_id)
    system = Aircraftsystem.objects.get(pk=system_id)
    # Tables of graphics
    allgraphics = Systemgraphic.objects.filter(aircraftsystem_id=system_id).order_by('media_label', 'version')
    for graphic in allgraphics:
        graphic.booked = Graphicworkdone.objects.filter(systemgraphic_id=graphic.id).aggregate(booked=Sum('hours_expended'))
    
    holdgraphics = Systemgraphic.objects.filter(aircraftsystem_id=system_id).filter(status__in=['Not Started','In Progress']).filter(on_hold=1).order_by('media_label', 'version')
    for graphic in holdgraphics:
        graphic.booked = Graphicworkdone.objects.filter(systemgraphic_id=graphic.id).aggregate(booked=Sum('hours_expended'))

    graphics = Systemgraphic.objects.filter(aircraftsystem_id=system_id).filter(status__in=['Not Started','In Progress']).order_by('media_label', 'version')
    for graphic in graphics:
        graphic.booked = Graphicworkdone.objects.filter(systemgraphic_id=graphic.id).aggregate(booked=Sum('hours_expended'))
        
        if graphic.adjusted_hours is None:
            graphic.adjusted_hours = 0
        if graphic.booked["booked"] is None:
            graphic.booked["booked"] = 0
        graphic.delta = graphic.adjusted_hours - graphic.booked["booked"]
        
    inprogress = Systemgraphic.objects.filter(aircraftsystem_id=system_id).filter(status__in=['In Progress']).order_by('media_label', 'version')
    for graphic in inprogress:
        graphic.booked = Graphicworkdone.objects.filter(systemgraphic_id=graphic.id).aggregate(booked=Sum('hours_expended'))

    inqa = Systemgraphic.objects.filter(aircraftsystem_id=system_id, status__in=['Development Completed','TechnicalReview','EditorialReview','InternalQA','UploadedToLCMS','ExternalReview']).order_by('media_label', 'version')
    for graphic in inqa:
        graphic.booked = Graphicworkdone.objects.filter(systemgraphic_id=graphic.id).aggregate(booked=Sum('hours_expended'))

    complete = Systemgraphic.objects.filter(aircraftsystem_id=system_id).filter(status__in=['Locked']).order_by('media_label', 'version')
    for graphic in complete:
        graphic.booked = Graphicworkdone.objects.filter(systemgraphic_id=graphic.id).aggregate(booked=Sum('hours_expended'))

    # Header Calculations
    adjest = Systemgraphic.objects.filter(aircraftsystem_id=system_id).aggregate(adjustedestimate=Sum('adjusted_hours'))
    est = Systemgraphic.objects.filter(aircraftsystem_id=system_id).aggregate(estimate=Sum('estimated_hours'))
    booked = Graphicworkdone.objects.filter(systemgraphic_id__in=allgraphics).aggregate(booked=Sum('hours_expended'))
    # Tables of comments
    comments = Comments.objects.filter(source='system', source_id=system_id,)
    uploads = Uploads.objects.filter(source='system', source_id=system_id,)
    return render(request, 'aircraftsystems/view.html', {'aircrafttype': type, 'system': system, 'allgraphics': allgraphics, 'inprogress': inprogress, 'graphics': graphics, 'holdgraphics': holdgraphics, 'inqa': inqa, 'completed': complete, 'adjest': adjest, 'est': est, 'booked': booked, 'comments': comments, 'uploads': uploads,})
    
# ################
# Graphic Views  #
# ################

@login_required    
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

@login_required    
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

@login_required
def graphicview(request, type_id, system_id, graphic_id):
    type = Aircrafttype.objects.get(pk=type_id)
    system = Aircraftsystem.objects.get(pk=system_id)
    graphic = Systemgraphic.objects.get(pk=graphic_id)
    works = Graphicworkdone.objects.filter(systemgraphic_id=graphic_id)
    comments = Comments.objects.filter(source='graphic', source_id=graphic_id,)
    uploads = Uploads.objects.filter(source='graphic', source_id=graphic_id,)
    return render(request, 'systemgraphics/view.html', {'aircrafttype': type, 'system': system, 'graphic': graphic, 'works': works, 'comments': comments, 'uploads': uploads,})

@login_required
def graphicdone(request, type_id, system_id, graphic_id):
    type = Aircrafttype.objects.get(pk=type_id)
    system = Aircraftsystem.objects.get(pk=system_id)
    graphic = Systemgraphic.objects.get(pk=graphic_id)
    Systemgraphic.objects.filter(id=graphic_id).update(status='Development Completed',)
    query = Comments(source='graphic', source_id=graphic_id, comment='*** DEVELOPMENT COMPLETE ***', created_by=request.user.get_full_name(), comment_type='Notification', comment_version=graphic.version,)
    query.save()
    works = Graphicworkdone.objects.filter(systemgraphic_id=graphic_id)
    return redirect('systemview', type_id=type.id, system_id=system.id,)

@login_required
def graphicholdtoggle(request, type_id, system_id, graphic_id):
    type = Aircrafttype.objects.get(pk=type_id)
    system = Aircraftsystem.objects.get(pk=system_id)
    graphic = Systemgraphic.objects.get(pk=graphic_id)
    if graphic.on_hold:
        Systemgraphic.objects.filter(id=graphic_id).update(on_hold=0,)
        query = Comments(source='graphic', source_id=graphic_id, comment='*** TAKEN OFF HOLD ***', created_by=request.user.get_full_name(), comment_type='Notification', comment_version=graphic.version,)
        query.save()
    else:
        Systemgraphic.objects.filter(id=graphic_id).update(on_hold=1,)
        query = Comments(source='graphic', source_id=graphic_id, comment='*** PLACED ON HOLD ***', created_by=request.user.get_full_name(), comment_type='Notification', comment_version=graphic.version,)
        query.save()
    works = Graphicworkdone.objects.filter(systemgraphic_id=graphic_id)
    return redirect('systemview', type_id=type.id, system_id=system.id,)

# ################
# Work Views     #
# ################

@login_required    
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
            query = Graphicworkdone(systemgraphic=graphic, work_carried_out=cd['work_carried_out'], created_by=request.user.get_full_name(), hours_expended=cd['hours_expended'],)
            query.save()
            Systemgraphic.objects.filter(id=graphic_id).update(last_update_by=request.user.get_full_name(),)
            Systemgraphic.objects.filter(id=graphic_id).update(status='In Progress',)
            return HttpResponseRedirect(reverse('graphicview', args=(type_id, system_id, graphic_id)))    
    else:
        form = WorkAddForm()
    return render(request, 'graphicwork/add.html', {'form': form})

@login_required    
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
            Graphicworkdone.objects.filter(id=work_id).update(systemgraphic=graphic, work_carried_out=cd['work_carried_out'], modified_by=request.user.get_full_name(), hours_expended=cd['hours_expended'],)
            return HttpResponseRedirect(reverse('graphicview', args=(type_id, system_id, graphic_id)))    
    else:
        work = Graphicworkdone.objects.get(id=work_id)
        dictionary = model_to_dict(work, fields=[], exclude=[])
        form = WorkEditForm(initial=dictionary)
    return render(request, 'graphicwork/edit.html', {'form': form})
    
    
# ################
# Comment Views  #
# ################

@login_required    
def commentadd(request, type_id, system_id, graphic_id=0, graphic_version=0, source='a', commenttype='a'):
    if source == 'system':
        if 'cancel' in request.POST:
                return HttpResponseRedirect(reverse('systemview', args=(type_id, system_id))) 
        if request.method == 'POST':
            form = CommentAddForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                type = Aircrafttype.objects.get(id=type_id)
                system = Aircraft3Dsystem.objects.get(id=system_id)
                query = Comments(source=source, source_id=system_id, comment=cd['comment'], created_by=request.user.get_full_name(), comment_type=commenttype, comment_version=0,)
                query.save()
                return HttpResponseRedirect(reverse('systemview', args=(type_id, system_id)))    
        else:
            form = CommentAddForm()
        return render(request, 'comments/add.html', {'form': form})
    elif source == '3Dsystem':
        if 'cancel' in request.POST:
                return HttpResponseRedirect(reverse('systemview3d', args=(type_id, system_id))) 
        if request.method == 'POST':
            form = CommentAddForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                type = Aircrafttype.objects.get(id=type_id)
                system = Aircraftsystem.objects.get(id=system_id)
                query = Comments(source=source, source_id=system_id, comment=cd['comment'], created_by=request.user.get_full_name(), comment_type=commenttype, comment_version=0,)
                query.save()
                return HttpResponseRedirect(reverse('systemview3d', args=(type_id, system_id)))    
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
                query = Comments(source=source, source_id=graphic_id, comment=cd['comment'], created_by=request.user.get_full_name(), comment_type=commenttype, comment_version=graphic_version,)
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
                query = Comments(source=source, source_id=graphic_id, comment=cd['comment'], created_by=request.user.get_full_name(), comment_type=commenttype, comment_version=graphic_version,)
                query.save()
                return HttpResponseRedirect(reverse('qaview', args=(type_id, system_id, graphic_id)))    
        else:
            form = CommentAddForm()
        return render(request, 'comments/add.html', {'form': form})    

# ################
# Upload Views   #
# ################
        
@login_required    
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
    if source == '3Dsystem':
        view_url = reverse('systemview3d', args=(type_id, system_id))
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('systemview3d', args=(type_id, system_id)))
        # Handle file upload
        if request.method == 'POST':
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                type = Aircrafttype.objects.get(id=type_id)
                system = Aircraft3Dsystem.objects.get(id=system_id)
                newdoc = Uploads(file = request.FILES['filename'], description=cd['description'], source=source, source_id=system_id )
                newdoc.save()
                # Redirect to the document list after POST
                return HttpResponseRedirect(reverse('systemview3d', args=(type_id, system_id)))
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
    
@login_required
def download_handler(request, pk):
    upload = get_object_or_404(Uploads, pk=pk)
    return serve_file(request, upload.file)    
    
    
# ################
# QA Views       #
# ################    

@login_required    
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

@login_required
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
            QA.objects.filter(pk=qa_id).update(result=result, created_by=request.user.get_full_name())
            return redirect('systemview', type_id=type.id, system_id=system.id)
        QA.objects.filter(pk=qa_id).update(result=result, created_by=request.user.get_full_name())
    else:
        QA.objects.filter(pk=qa_id).update(result=result, created_by=request.user.get_full_name())
        Systemgraphic.objects.filter(id=graphic_id).update(status='In Progress',)
        query = Comments(source='graphic', source_id=graphic_id, comment='*** QA FAIL ***', created_by=request.user.get_full_name(), comment_type='Notification', comment_version=graphic.version,)
        query.save()
        return redirect('systemview', type_id=type.id, system_id=system.id)
    
    return redirect('qaview', type_id=type.id, system_id=system.id, graphic_id=graphic.id)
    
    
# ################
# User Views     #
# ################      
    
@login_required
def logout_view(request):
    logout(request)    
    return redirect('login')
    
@login_required
def create_login(request):
    if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('allusers'))    
    if request.method == 'POST':
        form = NewLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            lNewUser = User.objects.create_user(cd['username'], 'dummy@email.com', cd['password'])
            lNewUser.first_name = cd['first_name']
            lNewUser.last_name = cd['last_name']
            lNewUser.groups.add(cd['groups'])
            lNewUser.save()
            return HttpResponseRedirect(reverse('allusers'))
    else:
        form = NewLoginForm()
    return render(request, 'registration/newuser.html', {'form': form})
    
@login_required
def change_password(request, user_id, source):
    if 'cancel' in request.POST:
        if source == 'usermanager':
            return HttpResponseRedirect(reverse('allusers'))
        return HttpResponseRedirect(reverse('home'))     
    if request.method == 'POST':
        form = PasswordChange(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
           
            u = User.objects.get(pk = user_id)
            u.set_password(cd['password'])
            u.save()
            if source == 'usermanager':
                return HttpResponseRedirect(reverse('allusers'))
            return HttpResponseRedirect(reverse('home'))
    else:
        form = PasswordChange()
    return render(request, 'registration/passwordchange.html', {'form': form})
    
@login_required
def userindex(request):
    listofusers = User.objects.all()
    return render(request, 'registration/index.html', {'listofusers': listofusers})
    
    
@login_required    
def edit_user(request, user_id):
    if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('allusers'))    
    if request.method == 'POST':
        form = UserEdit(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.filter(id=user_id).update(username = cd['username'], first_name=cd['first_name'], last_name=cd['last_name'],)
            lUser = User.objects.get(id=user_id)
            lUser.groups.clear()
            lUser.groups.add(cd['groups'])
            lUser.save()
            return HttpResponseRedirect(reverse('allusers'))
    else:
        lUser = User.objects.get(id=user_id)
        dictionary = model_to_dict(lUser, fields=[], exclude=[])
        form = UserEdit(initial=dictionary)
    return render(request, 'registration/useredit.html', {'form': form})
 
# ################
# CSV Views      #
# ################     

@login_required  
def typeimport(request): 
    view_url = reverse('typeindex')
    if 'cancel' in request.POST:
        return HttpResponseRedirect(reverse('typeindex'))
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            file = cd['filename']
            
            with file as f:
                reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
                for row in reader:

                    if Aircrafttype.objects.filter(name=row[0]).count() > 0:
                        type = Aircrafttype.objects.get(name=row[0])
                        Aircrafttype.objects.filter(id=type.id).update(name=row[0], description=row[1],)
                    else:                
                        query = Aircrafttype(name=row[0], description=row[1])
                        query.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('typeindex'))
    else:
        form = ImportForm() # A empty, unbound form
    return render(request, 'csvimport/add.html', {'form': form})


@login_required
def systemimport(request, type_id):
    view_url = reverse('typeview', args=(type_id,))
    if 'cancel' in request.POST:
        return HttpResponseRedirect(reverse('typeview', args=(type_id,)))
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            file = cd['filename']
            
            with file as f:
                reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
                for row in reader:
                    type = Aircrafttype.objects.get(id=type_id)
                    
                    nme = row[0]
                    desc = row[1]
                    wrk = row [2]
                    
                    if Aircraftsystem.objects.filter(aircrafttype=type.id, name=nme).count() > 0:
                        system = Aircraftsystem.objects.get(aircrafttype=type.id, name=nme)
                        
                        if system.description != desc:
                            query = Comments(source='system', source_id=system.id, comment='*** Description Changed ***\nFrom: "' + system.description + '"\nTo: "' + desc + '"', created_by=request.user.get_full_name(), comment_type='Importer', comment_version=0,)
                            query.save()
                        if system.workshare != wrk:
                            query = Comments(source='system', source_id=system.id, comment='*** Workshare Changed ***\nFrom: "' + system.workshare + '"\nTo: "' + wrk + '"', created_by=request.user.get_full_name(), comment_type='Importer', comment_version=0,)
                            query.save()
                                                
                        
                        Aircraftsystem.objects.filter(id=system.id).update(aircrafttype=type, name=nme, description=desc, workshare=wrk,)
                    else:
                        query = Aircraftsystem(aircrafttype=type, name=nme, description=desc, workshare=wrk,)
                        query.save()
                        system = Aircraftsystem.objects.get(aircrafttype=type.id, name=nme)
                        query = Comments(source='system', source_id=system.id, comment='*** Initial Import ***', created_by=request.user.get_full_name(), comment_type='Importer', comment_version=0,)
                        query.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('typeview', args=(type_id,)))
    else:
        form = ImportForm() # A empty, unbound form
    return render(request, 'csvimport/add.html', {'form': form})                  

@login_required
def graphicimport(request, type_id, system_id):
    view_url = reverse('systemview', args=(type_id, system_id))
    if 'cancel' in request.POST:
        return HttpResponseRedirect(reverse('systemview', args=(type_id, system_id)))
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            file = cd['filename']
            
            with file as f:
                reader = csv.reader(f, dialect='excel')
                firstline = True
                for row in reader:
                    if firstline:
                        firstline = False
                        continue
                    type = Aircrafttype.objects.get(id=type_id)
                    system = Aircraftsystem.objects.get(id=system_id)
                    
                    ml = row[0]
                    tpt = row[1]
                    kpt = row[2]
                    desc = row[3]
                    est = row[4]
                    adj = row[5]
                    
                    titleo = tpt + ' - ' + kpt
                    
                    if not adj:
                        adj = est
                    
                    if 'Maintenance Holding Graphic' in ml:
                        continue
                    if Systemgraphic.objects.filter(aircraftsystem=system.id, media_label=ml).count() > 0:
                        # Update existing
                        graphic = Systemgraphic.objects.get(aircraftsystem=system.id, media_label=ml)
                        
                        if graphic.title != titleo:
                            query = Comments(source='graphic', source_id=graphic.id, comment='*** Title Changed ***\nFrom: "'+graphic.title+'"\nTo: "'+titleo+'"', created_by=request.user.get_full_name(), comment_type='Importer', comment_version=graphic.version,)
                            query.save()
                        if graphic.description != desc:
                            query = Comments(source='graphic', source_id=graphic.id, comment='*** Description Changed ***\nFrom: "' + graphic.description + '"\nTo: "' + desc + '"', created_by=request.user.get_full_name(), comment_type='Importer', comment_version=graphic.version,)
                            query.save()
                            
                        if graphic.title != titleo or graphic.description != desc:
                            Systemgraphic.objects.filter(id=graphic.id).update(aircraftsystem=system, media_label=ml, title=titleo, description=desc, estimated_hours=est, adjusted_hours=adj, last_update_by=request.user.get_full_name() + '\n**Importer**', )
                    else:
                        # New Record to Import
                        query = Systemgraphic(aircraftsystem=system, media_label=ml, title=titleo, description=desc, estimated_hours=est, adjusted_hours=adj, last_update_by=request.user.get_full_name() + '\n**Importer**', )
                        query.save()
                        graphic = Systemgraphic.objects.get(aircraftsystem=system.id, media_label=ml)
                        query = Comments(source='graphic', source_id=graphic.id, comment='*** Initial Import ***', created_by=request.user.get_full_name(), comment_type='Importer', comment_version=graphic.version,)
                        query.save()
                        
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('systemview', args=(type_id, system_id)))
    else:
        form = ImportForm() # A empty, unbound form
    return render(request, 'csvimport/add.html', {'form': form})              

@login_required
def systemimport3d(request, type_id):
    view_url = reverse('type3dview', args=(type_id,))
    if 'cancel' in request.POST:
        return HttpResponseRedirect(reverse('type3dview', args=(type_id,)))
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            file = cd['filename']
            
            with file as f:
                reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
                for row in reader:
                    type = Aircrafttype.objects.get(id=type_id)
                    
                    nme = row[0]
                    desc = row[1]
                    
                    if Aircraft3Dsystem.objects.filter(aircrafttype=type.id, name=nme).count() > 0:
                        system = Aircraft3Dsystem.objects.get(aircrafttype=type.id, name=nme)
                        
                        if system.description != desc:
                            query = Comments(source='3Dsystem', source_id=system.id, comment='*** Description Changed ***\nFrom: "' + system.description + '"\nTo: "' + desc + '"', created_by=request.user.get_full_name(), comment_type='Importer', comment_version=0,)
                            query.save()
                        
                        Aircraft3Dsystem.objects.filter(id=system.id).update(aircrafttype=type, name=nme, description=desc, )
                    else:
                        query = Aircraft3Dsystem(aircrafttype=type, name=nme, description=desc, )
                        query.save()
                        system = Aircraft3Dsystem.objects.get(aircrafttype=type.id, name=nme)
                        query = Comments(source='3Dsystem', source_id=system.id, comment='*** Initial Import ***', created_by=request.user.get_full_name(), comment_type='Importer', comment_version=0,)
                        query.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('type3dview', args=(type_id,)))
    else:
        form = ImportForm() # A empty, unbound form
    return render(request, 'csvimport/add.html', {'form': form})                  

# ################
# System Views   #
# ################
	
@login_required
def systemadd3d(request, type_id):
    if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('type3dview', args=(type_id,)))    
    if request.method == 'POST':
        form = System3DAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            type = Aircrafttype.objects.get(id=type_id)
            query = Aircraft3Dsystem(aircrafttype=type, name=cd['name'], description=cd['description'],)
            query.save()
            return HttpResponseRedirect(reverse('type3dview', args=(type_id,)))
    else:
        form = System3DAddForm()
    return render(request, '3dsystems/add.html', {'form': form})

@login_required
def systemedit3d(request, type_id, system_id):
    if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse('type3dview', args=(type_id,)))   
    if request.method == 'POST':
        form = System3DEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            type = Aircrafttype.objects.get(id=type_id)
            Aircraft3Dsystem.objects.filter(id=system_id).update(aircrafttype=type, name=cd['name'], description=cd['description'],)
            return HttpResponseRedirect(reverse('type3dview', args=(type_id,)))
    else:
        system = Aircraft3Dsystem.objects.get(id=system_id)
        dictionary = model_to_dict(system, fields=[], exclude=[])
        form = System3DEditForm(initial=dictionary)
    return render(request, '3dsystems/edit.html', {'form': form})

@login_required
def systemview3d(request, type_id, system_id):
    type = Aircrafttype.objects.get(pk=type_id)
    system = Aircraft3Dsystem.objects.get(pk=system_id)
    
    currstatus = Status3D.objects.filter(aircraft3dsystem=system.id, ).order_by('id').reverse()[:1]

    if currstatus.count() == 0:
        row = Status3D(aircraft3dsystem=system, version=0,stage='CATIA_Extracted' )
        row.save()
        currstatus2 = currstatus.get()
    else:
        currstatus2 = currstatus.get()
    
    if currstatus2.stage == 'CATIA_Extracted' and currstatus2.result == 'Pass':
        Aircraft3Dsystem.objects.filter(pk=system_id).update(status=currstatus2.stage)
        row = Status3D(aircraft3dsystem=system, version=0, stage='3D_PDF_Created' )
        row.save()
        currstatus2 = currstatus.get()
        system = Aircraft3Dsystem.objects.get(pk=system_id)
        
    if currstatus2.stage == '3D_PDF_Created' and currstatus2.result == 'Pass':
        Aircraft3Dsystem.objects.filter(pk=system_id).update(status=currstatus2.stage)
        row = Status3D(aircraft3dsystem=system, version=0, stage='Checked_Against_Storyboard' )
        row.save()
        currstatus2 = currstatus.get()
        system = Aircraft3Dsystem.objects.get(pk=system_id)
        
    if currstatus2.stage == 'Checked_Against_Storyboard' and currstatus2.result == 'Pass':
        Aircraft3Dsystem.objects.filter(pk=system_id).update(status=currstatus2.stage)
        row = Status3D(aircraft3dsystem=system, version=0, stage='Converted_to_Max' )
        row.save()
        currstatus2 = currstatus.get()
        system = Aircraft3Dsystem.objects.get(pk=system_id)

    if currstatus2.stage == 'Converted_to_Max' and currstatus2.result == 'Pass':
        Aircraft3Dsystem.objects.filter(pk=system_id).update(status=currstatus2.stage)
        row = Status3D(aircraft3dsystem=system, version=0, stage='Rigged_For_Animation' )
        row.save()
        currstatus2 = currstatus.get()
        system = Aircraft3Dsystem.objects.get(pk=system_id)

    if currstatus2.stage == 'Rigged_For_Animation' and currstatus2.result == 'Pass':
        Aircraft3Dsystem.objects.filter(pk=system_id).update(status=currstatus2.stage)
        row = Status3D(aircraft3dsystem=system, version=0, stage='SME_Signed_Off' )
        row.save()
        currstatus2 = currstatus.get()
        system = Aircraft3Dsystem.objects.get(pk=system_id)

    if currstatus2.stage == 'SME_Signed_Off' and currstatus2.result == 'Pass':
        Aircraft3Dsystem.objects.filter(pk=system_id).update(status=currstatus2.stage)
        row = Status3D(aircraft3dsystem=system, version=0, stage='CATIA_Update_Required' )
        row.save()
        currstatus2 = currstatus.get()
        system = Aircraft3Dsystem.objects.get(pk=system_id)
        
    if currstatus2.stage == 'CATIA_Update_Required' and currstatus2.result == 'Pass':
        row = Status3D(aircraft3dsystem=system, version=0, stage='Complete' )
        row.save()
        currstatus2 = currstatus.get()
        Aircraft3Dsystem.objects.filter(pk=system_id).update(status=currstatus2.stage)
        system = Aircraft3Dsystem.objects.get(pk=system_id)
        
    if currstatus2.result == 'Fail':
        Aircraft3Dsystem.objects.filter(pk=system_id).update(status='Not Started')
        row = Status3D(aircraft3dsystem=system, version=0,stage='CATIA_Extracted' )
        row.save()
        currstatus2 = currstatus.get()
        system = Aircraft3Dsystem.objects.get(pk=system_id)
        
    statuss = Status3D.objects.filter(aircraft3dsystem=system.id, ).order_by('id')
    
    # Tables of comments
    comments = Comments.objects.filter(source='3Dsystem', source_id=system_id,)
    uploads = Uploads.objects.filter(source='3Dsystem', source_id=system_id,)
    
    return render(request, '3dsystems/view.html', {'aircrafttype': type, 'system': system, 'comments': comments, 'uploads': uploads, 'statuss': statuss})
        
@login_required
def result3d(request, type_id, system_id, version, stage, stage_id, result):
    type = Aircrafttype.objects.get(pk=type_id)
    system = Aircraft3Dsystem.objects.get(pk=system_id)
    
    if result == 'Pass':
        
        Status3D.objects.filter(pk=stage_id).update(result=result, created_by=request.user.get_full_name())
    else:
        Status3D.objects.filter(pk=stage_id).update(result=result, created_by=request.user.get_full_name())
        #Systemgraphic.objects.filter(id=system_id).update(status='In Progress',)
        #query = Comments(source='3Dsystem', source_id=graphic_id, comment='*** QA FAIL ***', created_by=request.user.get_full_name(), comment_type='Notification', comment_version=graphic.version,)
        #query.save()
        #return redirect('systemview', type_id=type.id, system_id=system.id)
    
    return redirect('systemview3d', type_id=type.id, system_id=system.id)
    
