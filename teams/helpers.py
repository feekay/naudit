from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.forms.models import modelformset_factory

from teams.helpers import *
from teams.forms import *
from teams.models import *

import json
from django.core import serializers

#------------------------------------------------------------------------------#
def handle_pending(request, entry, user_type, context_dic):
    if request.method=="POST":
    #    print "Post", user_type
        if user_type == "b":
            entry.approved = True
            log_activity(request, entry,"Approved")
            entry.save()
            #return HttpResponseRedirect('/main')
        if user_type == "c":
            entry.cleared = True
            log_activity(request, entry, "Accepted")
            entry.save()
        if user_type =="s":
            entry.verified = True
            log_activity(request, entry, "Verified")
            entry.save()
        return HttpResponseRedirect('/main')
    return render(request, 'pending_entry.html', context_dic)

#------------------------------------------------------------------------------#
def handle_member_change(request):
    try:
        member_inst = Member.objects.get(user= request.user)
    except Member.DoesNotExist:
        return None
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member_inst)
        if form.is_valid():
            member =form.save(commit=False)
            member.save()
            log_activity(request,action="Info updated")
            form = MemberForm(instance=member_inst)
    else:
        form = MemberForm(instance=member_inst)
    return form
#------------------------------------------------------------------------------#
def handle_password_change(request):
    if request.method == "POST" \
    and 'old_password' in request.POST \
    and 'new_password' in request.POST:
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        user = authenticate(username = request.user.username, password = old_password)
        
        if user is not None:
            if user.is_active:
                user.set_password(new_password)
                user.save()
                login(request, user)
                return True
        else:
            return False  
        
    else:
        return None
#------------------------------------------------------------------------------#
def get_entries(team="a"):
    if team =="a":
        return Entry.objects.filter(visited = False)
    elif team =="b":
        return Entry.objects.filter(approved = True, completed = False)
    elif team =="c":
        return Entry.objects.filter(visited = True, cleared = True, verified = False)
    #Super User
    elif team =="s":
        return Entry.objects.all()

#------------------------------------------------------------------------------#

def get_pending(team="b"):
    if team =="b":
        return Entry.objects.filter(approved = False)
    elif team =="c":
        return Entry.objects.filter(visited = True, cleared = False)
    #Super User
    elif team =="s":
        return Entry.objects.filter(completed = True, verified= False)
#------------------------------------------------------------------------------#

def get_complete(team="a"):
    if team =="a":
        return Entry.objects.filter(approved = True).exclude(finalized = True)
    elif team =="b":
        return Entry.objects.filter(cleared = True).exclude(finalized = True)
    elif team =="c":
        return Entry.objects.filter(verified = True).exclude(finalized = True)
    #Super User
    elif team =="s":
        return Entry.objects.filter(finalized= True)

#------------------------------------------------------------------------------#
def get_employee_type(member):
    try:
        temp = Salary_based.objects.get(details = member)
    except:
        pass
    else:
        user_type = "sal"
        
    try:
        temp = Entry_based.objects.get(details = member)
    except:
        pass
    else:
        user_type = "ent"

    return user_type

#------------------------------------------------------------------------------#        
def get_member_type(user):
    if user.is_superuser:
        user_type = "s"
    else:
        member = Member.objects.get(user=user)
        user_type = member.member_type

    return user_type

#------------------------------------------------------------------------------#
def teamb_entry(request, entry):
    if entry.completed:
        return None

    try:
        member = Member.objects.get(user= request.user)
    except:
        return None

    if not edit_allowed(entry, member):
        return None

    AttachmentFormSet = modelformset_factory(Attachment, form=AttachmentForm)
    if request.method == 'POST':
        formset = AttachmentFormSet(request.POST, request.FILES,queryset=Attachment.objects.none())
        if formset.is_valid():
            instances= formset.save(commit=False)
            for instance in instances:
                instance.entry = entry
                instance.save()
            #print member
            member.bowner_set.add(entry)
            member.save()
    formset = AttachmentFormSet(queryset=Attachment.objects.none())
    return formset
#------------------------------------------------------------------------------#
def teamc_entry(request, entry):
    if entry.completed:
        return None

    try:
        member = Member.objects.get(user= request.user)
    except:
        return None
    if not edit_allowed(entry, member):
        return None
    
    CFormset = modelformset_factory(Attachment, CForm, max_num=0)
    if request.method=="POST":
        formset = CFormset(request.POST, queryset= Attachment.objects.filter(entry=entry))
        if formset.is_valid():
            instances = formset.save()
            log_activity(request, entry, action="Edited")
            member.cowner_set.add(entry)
            member.save()

    formset = CFormset(queryset= Attachment.objects.filter(entry=entry))
    return formset
#------------------------------------------------------------------------------#
def edit_allowed(entry, member):
    if member.member_type == "a" and entry.owner == member:
        return True
    if member.member_type == "b" and (entry.b_owner == member or entry.b_owner is None):
        return True
    elif member.member_type == "c" and(entry.c_owner == member or entry.c_owner is None):
        return True
    else:
        return False
#------------------------------------------------------------------------------#
def log_activity(request, obj=None, action="Created"):
    if obj:
        activity = Activity.objects.create(user= request.user.username, obj= str(obj), action=action)
    else:
        activity = Activity.objects.create(user= request.user.username, action=action)
    activity.save()


