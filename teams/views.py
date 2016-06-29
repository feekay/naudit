from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

from teams.forms import *
from teams.models import Entry, Company

# Create your views here.

#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_authenticated)
def home(request):
    context_dic ={}
    context_dic["user_type"]= get_member_type(request.user)
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
def add_entry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)

        member = Member.objects.get(user=request.user)
        #Get the type of member and set the verified status
        emp_type = get_employee_type(member)
        if emp_type == "sal":
            verified = True
        else:
            verified = False

        if form.is_valid():
            entry = form.save(commit=False)
            entry.owner = member
            entry.verified = verified
            entry.save()
            add_entry(entry, member)
            return HttpResponseRedirect('/main/entries')
    else:
        form = EntryForm()
    return render(request, "add_entry.html", {"form": form})

#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def edit_entry(request, entry_id):
    try:
        entry = Entry.objects.get(id= entry_id)
    except:
        return HttpResponse(status=404)
 
    if request.method == "POST":
        form = EntryForm(request.POST, instance = entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            return HttpResponseRedirect('/main/entries')
    else:
        form = EntryForm(instance = entry)
    return render(request, "add_entry.html", {"form": form})

#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_superuser)
def add_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company=form.save()
            return HttpResponseRedirect('/main/companies')
    else:
        form = CompanyForm()
    return render(request, "add_company.html", {"form": form})

#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_authenticated)
def add_route(request):
    if request.method == "POST":
        form = RouteForm(request.POST, request.FILES)

        if form.is_valid():
            route=form.save(commit=False)

            #Look for entries that have the same route date if none found. 
            #Don't Save the route and Raise a form error.
            entries = Entry.objects.filter(route_date = route.route_date)
            if entries:
                route.save()
                for entry in entries:
                    entry.route = route
                    entry.save()
                return HttpResponseRedirect('/main/routes')
            else:
                form.add_error("route_date", "No entries on given date")
                return render(request, "add_route.html", {"form": form})

    else:
        form = RouteForm()
    return render(request, "add_route.html", {"form": form})

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
    context_dic["member_type"]=user_type

    #Send forms accoding to scenario
    #If the pending page is open send approval form
    #Otherwise send forms to add attachments or approve attachment
    if pending:
        if request.method=="POST":
            print "Post", user_type
            if user_type == "b":
                entry.approved = True
                entry.save()
            if user_type == "c":
                entry.cleared = True
                entry.save()
            if user_type =="s":
                entry.finalized = True

        return render(request, 'pending_entry.html', context_dic)     
    else:     
        if user_type=="b":
            form  = teamb_entry(request, entry)
            context_dic["form"] = form
        elif user_type=="c":
            form = teamc_entry(request)
            context_dic["form"] = form
        else:
            return render(request, "view_entry.html", context_dic)
        if form is None:
            return HttpResponseRedirect('/main/entries')
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

@user_passes_test(lambda u: u.is_authenticated)
def companies_view(request):
    context_dic = {}
    context_dic["companies"]=Company.objects.all()
    return render(request, "view_companies.html", context_dic)

#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_authenticated)
def members_view(request):
    context_dic = {}
    context_dic["members"]=Member.objects.all()
    return render(request, "view_members.html", context_dic)

#------------------------------------------------------------------------------#

@user_passes_test(lambda u: u.is_authenticated)
def routes_view(request):
    context_dic = {}
    context_dic["routes"]=Route.objects.all()
    return render(request, "view_routes.html", context_dic)

#------------------------------------------------------------------------------#
@user_passes_test(lambda u: u.is_authenticated)
def pending_view(request):
    context_dic = {}

    user_type = get_member_type(request.user)

    context_dic["entries"]=get_pending(team = user_type)
    
    #Generates links on template based on 'page'
    context_dic["page"] = "pending"
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
    logout(request)
    return HttpResponseRedirect('/main/login')

#------------------------------------------------------------------------------#
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            if user.is_active:
                login(request, user)
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
    if request.method == "POST":
        #username = request.POST['username']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        user = authenticate(username = request.user.username, password = old_password)
        
        if user is not None:
            if user.is_active:
                user.set_password(new_password)
                user.save()
                context_dic['alert'] = 'Password change successful'
        else:
            context_dic['alert'] = 'An error occured while changing password'  
        
    else:
        context_dic['form'] = SettingsForm()
        context_dic['alert'] =''
    return render(request, "settings.html", context_dic)

#------------------------------------------------------------------------------#
def get_entries(team="a"):
    if team =="a":
        return Entry.objects.filter(visited = False)
    elif team =="b":
        return Entry.objects.filter(approved = True, completed = False)
    elif team =="c":
        return Entry.objects.filter(visited = True, cleared = True, finalized = False)
    #Super User
    elif team =="s":
        return Entry.objects.all()

#------------------------------------------------------------------------------#

def get_pending(team="b"):
    if team =="b":
        return Entry.objects.filter(approved = False, visited = False)
    elif team =="c":
        return Entry.objects.filter(visited = True, cleared = False, completed = False)
    #Super User
    elif team =="s":
        return Entry.objects.filter(completed = True, finalized= False)

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

    try:
        member = Member.objects.get(user=user)
    except:
        return None
    #Check employee type and set the value of clear
    employee = get_employee_type(member)
    if employee == "sal":
        cleared = True
    else:
        cleared = False

    if request.method == "POST":
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            for f in request.FILES.getlist('file'):
                Attachment.objects.create(entry=entry, item=f)
            entry.visited = True
            entry.cleared = cleared
            entry.save()
            #Attach entry entry to member
            add_entry(entry, member)
            return None
    else:
        form = MyForm()
    return form

#------------------------------------------------------------------------------#
def teamc_entry(request):
    pass

#------------------------------------------------------------------------------#
def add_entry(entry, member):
    if get_employee_type(member) == "ent":
        try:
            emp = Entry_based.objects.get(details = member)
        except:
            pass
        else:
            emp.entries.add(entry)
            emp.save()

#------------------------------------------------------------------------------#
