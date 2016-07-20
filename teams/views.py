from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

from teams.helpers import *
from teams.forms import *
from teams.models import Entry, Company

import json
from django.core import serializers
# Create your views here.


#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_authenticated)
def home(request):
    context_dic={}
    return render(request, "index.html", context_dic)

#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_superuser)
def add_member(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        form2 = MemberForm(request.POST, request.FILES)
        form3 = TypeForm(request.POST)

        if form.is_valid() and form2.is_valid() and form3.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            member = form2.save(commit=False)
            member.user = user
            member.save()

            user_type = form3.cleaned_data['source']
            if user_type == "s":
                salary = form3.cleaned_data['salary']
                Salary_based.objects.create(details= member, salary = salary)
            elif user_type == "e":
                rate = form3.cleaned_data['rate']
                Entry_based.objects.create(details = member, rate =rate)

            return HttpResponseRedirect('/main/members')
    else:
        form = UserForm()
        form2 = MemberForm()
        form3 = TypeForm()
    return render(request, "add_member.html", {"form": form, "form2": form2,"form3": form3})

#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_authenticated)
def create_entry(request):
    context_dic={}
    if request.method == "POST":
        form = EntryForm(request.POST)

        member = Member.objects.get(user=request.user)
        #Get the type of member and set the verified status
        emp_type = get_employee_type(member)
        if emp_type == "sal":
            approved = True
        else:
            approved = False

        if form.is_valid():
            entry = form.save(commit=False)
            entry.owner = member
            entry.approved = approved
            entry.save()
            log_activity(request, entry)
            return HttpResponseRedirect('/main/')
    else:
        form = EntryForm()
    context_dic['form'] = form
    return render(request, "add_entry.html",context_dic)

#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def edit_entry(request, entry_id):
    context_dic ={}
    try:
        member = Member.objects.get(user= request.user)
    except:
        return HttpResponse(status=404)
    else:
        emp_type = get_employee_type(member)
    try:
        entry = Entry.objects.get(id= entry_id)
    except:
        return HttpResponse(status=404)
    if not edit_allowed(member):
        return HttpResponseRedirect('/main/entries')

    if request.method == "POST":
        form = EntryForm(request.POST, instance = entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            log_activity(request,entry, "Edited")
            return HttpResponseRedirect('/main/entries')
    else:
        context_dic['form'] = EntryForm(instance = entry)
    return render(request, "add_entry.html", context_dic)

#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def verify_entry(request, entry_id):
    context_dic= {}

    try:
        member = Member.objects.get(user= request.user)
    except:
        return HttpResponse(status=404)
    else:
        emp_type = get_employee_type(member)

    try:
        entry = Entry.objects.get(id = entry_id)
    except:
        return HttpResponse(status=404)

    user_type = get_member_type(request.user)

    if emp_type == "sal":
        pending = True
    else:
        pending = False

    if user_type == "b":
        entry.visited = True
        entry.cleared = pending
        entry.save()
    elif user_type == "c":
        entry.completed = True
        entry.verified = pending
        entry.save()
    elif user_type == "s":
        entry.finalized = True
        entry.save()
    return HttpResponseRedirect('/main/entries')
#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_superuser)
def add_company(request):
    context_dic={}
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company=form.save()
            log_activity(request,company)
            return HttpResponseRedirect('/main/companies')
    else:
        context_dic['form'] = CompanyForm()
    return render(request, "add_company.html", context_dic)

#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_authenticated)
def add_route(request):
    context_dic={}
    if request.method == "POST":
        form = RouteForm(request.POST, request.FILES)

        if form.is_valid():
            route=form.save(commit=False)

            #Look for entries that have the same route date if none found. 
            #Don't Save the route and Raise a form error.
            entries = Entry.objects.filter(route_date = route.route_date)
            if entries:
                route.save()
                log_activity(request,route)
                for entry in entries:
                    entry.route = route
                    entry.save()
                    log_activity(request,entry, "Route Added")
                return HttpResponseRedirect('/main/routes')
            else:
                form.add_error("route_date", "No entries on given date")
                return render(request, "add_route.html", {"form": form})
        else:
            context_dic['form'] = form
    else:
        context_dic['form'] = RouteForm()
    return render(request, "add_route.html", context_dic)

#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def add_quiz(request):
    context_dic={}
    return render(request, "add_quiz.html", context_dic)

#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def quiz(request):
    return render(request, "quiz.html", {})

#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def activity(request):
    context_dic ={}
    context_dic['activites'] = Activity.objects.all().order_by('time')
    return render(request, "activity.html", context_dic)


#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def entry(request, entry_id, pending=False):
    context_dic = {}
    try:
        entry = Entry.objects.get(id=entry_id)
        context_dic["entry"] = entry
    except:
        return HttpResponse(status=404)

    user_type = get_member_type(request.user)

    #Send forms accoding to scenario
    #If the pending page is open send approval form
    #Otherwise send forms to add attachments or approve attachment
    if pending:
        return handle_pending(request, entry, user_type, context_dic)
    else:     
        if user_type=="b":
            formset  = teamb_entry(request, entry)
            context_dic["formset"] = formset
            context_dic["attachments"] = Attachment.objects.filter(entry = entry)
        elif user_type=="c":
            formset = teamc_entry(request, entry)
            context_dic["formset"] = formset
            context_dic["attachments"] = Attachment.objects.filter(entry = entry)
        else:
            return render(request, "view_entry.html", context_dic)
        #if formset is None:
        #    return HttpResponseRedirect('/main/entries')
    return render(request, "view_entry.html", context_dic)
#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_authenticated)
def entries_view(request):
    context_dic = {}
    user_type = get_member_type(request.user)

    context_dic["entries"]=get_entries(team = user_type)

    #Generates links on template based on 'page'
    context_dic["page"] = "entries"
    return render(request, "view_entries.html", context_dic)

#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_superuser)
def companies_view(request):
    context_dic = {}
    context_dic["companies"]=Company.objects.all()
    return render(request, "view_companies.html", context_dic)

#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_superuser)
def members_view(request):
    context_dic = {}
    context_dic["members"]=Member.objects.all()
    return render(request, "view_members.html", context_dic)

#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_authenticated)
def routes_view(request):
    context_dic = {}
    context_dic["routes"]=Route.objects.all()
    context_dic["page"] ="routes"
    return render(request, "view_routes.html", context_dic)
#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_authenticated)
def route_view(request, route_id):
    context_dic = {}
    route = Route.objects.get(id= route_id)
    context_dic["route"]= route
    context_dic["entries"]= route.entry_set.all()
    #print route.entry_set.count()
    return render(request, "view_route.html", context_dic)
#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_authenticated)
def pending(request):
    context_dic = {}
    user_type = get_member_type(request.user)
    if user_type == 'b':
        context_dic["routes"]=Route.objects.all()
    
        context_dic["page"] ="pend"
        return render(request, "view_routes.html", context_dic)
    else:
        return pending_view(request)

#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def pending_view(request, route_id=None):
    context_dic = {}
    
    user_type = get_member_type(request.user)

    if route_id:
        route = Route.objects.get(id= route_id)
        context_dic["entries"]=get_pending(team = user_type, route=route)

    else:
        context_dic["entries"]=get_pending(team = user_type)

    #Generates links on template based on 'page'
    context_dic["page"] = "pending"
    return render(request, "view_entries.html", context_dic)
#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def complete_view(request):
    context_dic = {}
    
    user_type = get_member_type(request.user)

    context_dic["entries"]=get_complete(team = user_type)
    
    #Generates links on template based on 'page'
    context_dic["page"] = "entries"
    return render(request, "view_entries.html", context_dic)
#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def finish_view(request):
    context_dic = {}

    context_dic["entries"]=Entry.objects.filter(finalized= True)
    context_dic["page"] = "entries"
    return render(request, "view_entries.html", context_dic)
#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_superuser)
def emp_entries(request):
    employees = Entry_based.objects.all()
    context_dic ={}
    emps=[]
    for employee in employees:
        temp = {}
        temp["count"] = employee.entry_count()
        temp["name"] = employee.details.user.first_name
        emps.append(temp)
    context_dic["employees"] = emps

    return render(request, 'count.html', context_dic)
#------------------------------------------------------------------------------#
def logout_view(request):
    log_activity(request,None, "Logged out")
    logout(request)
    return HttpResponseRedirect('/main/login')

#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            if user.is_active:
                login(request, user)
                log_activity(request,action= "Logged in")
                return HttpResponseRedirect('/main')
            else:
                return HttpResponse("Account has been deactivated")
        else:
            return HttpResponse("Invalid Username or Password")

    else:
        return render(request, "login.html", {})
        
#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def settings(request):
    context_dic ={}
    context_dic['c_user']= request.user.username
    
    status = handle_password_change(request)
    
    if status is None:
        context_dic['password_form'] = SettingsForm()
    elif status is True:
        context_dic['password_form'] = SettingsForm()
        context_dic['alert'] ="Password Successfully Changed"
        log_activity(request,action= "Password Changed")
    else:
        context_dic['password_form'] = SettingsForm()
        context_dic['alert'] ="Password Change Attempt Failed"
    if not request.user.is_superuser:
        context_dic['member_form'] = handle_member_change(request)

    return render(request, "settings.html", context_dic)
#------------------------------------------------------------------------------#
################################################################################
#  MESSAGING RELATED FUNCTIONS
################################################################################

@user_passes_test(lambda u: u.is_authenticated)
def messages(request):
    context_dic ={}
    return render(request,'messages.html' ,context_dic)

#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def send_message(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception as inst:
            #print(inst)
            pass

        message = data['message']
        text = message
        frm = request.user

        try:
            message = Message.objects.create(
            time = datetime.now(),
            text = text,
            frm = frm,
            )

            mentions = data['mentions']

            for user_id in mentions:
                try:
                    user=User.objects.get(id = user_id)
                except:
                    #print("No such User")
                    pass
                else:
                    message.to.add(user)
                    message.save()
                    #print(message.to.all())

            message.save()
        except Exception as inst:
            #print(inst)
            return HttpResponse(status=404)
        #print("Create")
        return HttpResponse(status=200)
    return HttpResponse(status = 404)
#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def get_messages(request, limit= None):
    try:
        limit = int(limit)
    except:
        limit= 30

    username = request.user
    user = User.objects.get(username = username)
    if user.is_superuser:
        messages = Message.objects.all().order_by('time')
        #data = serializers.serialize('json', messages)
        #return HttpResponse(data, content_type='application/json')        
    else:
        messages = Message.objects.all().filter(Q(to = user)|Q(to=None)|Q(frm=user)).order_by('time')

    if limit:
        messages = messages[:limit]

    try:
        return render(request,'messages_body.html',{'messages': messages})
    except:
        return HttpResponse("Error in template")


#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def get_member_list(max_results =0, starts_with=""):
    user_list = []
    staff_list = []
#    print("Searching for staff", starts_with)
    if starts_with:
        user_list = User.objects.filter(first_name__istartswith=starts_with)
        for user in user_list:
            staff_list.append(Member.objects.get(user = user))
        #print(staff_list)
#    if max_results > 0:
#        if staff_list.count() > max_results:
#            staff_list = staff_list[:max_results]
    #print("Returning")
    return staff_list
#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def suggest_member(request):

    staff_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        #print("Request Recieved", starts_with)

    staff_list = get_member_list(4,starts_with)
    #print("Response Ready")
    data = serializers.serialize("json",staff_list)
    #print( data)
    return HttpResponse(data, content_type='application/json')

