from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import *
from .forms import *
import csv
import io
from django.views.decorators.clickjacking import xframe_options_sameorigin

#admin user check
def check_admin(user):
   return user.is_superuser

#home view
@xframe_options_sameorigin
def home(request):
    
    res_out = Research.objects.all()
   
    
    context = {
        "res_out": res_out,
    }
    return render(request, "all/home.html", context)

#edit profile view
def my_account(request):
    log_his = LoginHistory.objects.filter(end_user__user=request.user).order_by('login_date')
    user1 = EndUser.objects.get(user=request.user)
    form1 = EditUserForm(instance=user1)
    if request.method == 'POST':
        if 'btnupdateprofile' in request.POST:
            form1 = EditUserForm(request.POST, request.FILES, instance=user1)
            if form1.is_valid():
                form1.save()

                messages.success(request, "Account Updated.")
                return redirect("/my_account")
        else:
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')

            user = authenticate(request, username=request.user, password=old_password)
            if user is None:
                messages.error(request, "Wrong current password.")
                return redirect("/my_account")

            if new_password != confirm_new_password:
                messages.error(request, "The new password and confirm new password didn't match.")
                return redirect("/my_account")
            
            change_pass = request.user
            change_pass.set_password(new_password)
            end_users = EndUser.objects.get(user=change_pass)
            end_users.forgot_password_token = ""
            change_pass.save()
            end_users.save()
            logout(request)
            messages.success(request, "Password changed. Please, login with your username and new password.")
            return redirect("/login")

    context = {
        "form1": form1,
        "log_his":log_his
    }
    return render(request, "all/my_account.html", context)

##         START         ##
###                     ###
#### #####-ADMIN-##### ####
###                     ###
##         START         ##

#dashboard view 
@user_passes_test(check_admin)
def dashboard(request):
    end_users = EndUser.objects.filter(user=request.user, is_active=True)
    log_his = LoginHistory.objects.all()

    employed_faculty = EndUser.objects.filter(is_faculty=True, is_active=True)
    employed_admin = EndUser.objects.filter(is_admin=True, is_active=True)
    enrolled_student = EndUser.objects.filter(is_student=True, is_active=True)
    employed_faculty1 = employed_faculty.count()
    employed_admin1 = employed_admin.count()
    enrolled_student1 = enrolled_student.count()
    active_users = employed_faculty1 + enrolled_student1 + employed_admin1

    unemployed_faculty = EndUser.objects.filter(is_faculty=True, is_active=False)
    unemployed_admin = EndUser.objects.filter(is_admin=True, is_active=False)
    unenrolled_student = EndUser.objects.filter(is_student=True, is_active=False)
    unemployed_faculty1 = unemployed_faculty.count()
    unemployed_admin1 = unemployed_admin.count()
    unenrolled_student1 = unenrolled_student.count()
    inactive_users = unemployed_faculty1 + unenrolled_student1 + unemployed_admin1

    res_out = Research.objects.all()
    total_res_out = res_out.count()

    context = {
        "end_users": end_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "total_res_out": total_res_out,
        "log_his": log_his,
    }
    return render(request, "admin/dashboard/dashboard.html", context)

#add keyword view
@user_passes_test(check_admin)
def add_keyword(request):
    if request.method == 'POST':
        form = AddKeywordForm(request.POST)
        if form.is_valid():
            keyword_name = form.cleaned_data.get('keyword_name')
            if Keyword.objects.filter(keyword_name=keyword_name):
                messages.error(request, keyword_name + " is already added.")
                return redirect("reports:add_keyword")
            else:
                form.save()
                messages.success(request, ("Keyword successfully saved."))
                return redirect("reports:add_keyword")
    else:
        form = AddKeywordForm()
    context = {
        "form": form,
    }
    return render(request, "admin/dashboard/add_keyword.html", context)

#add research view
@user_passes_test(check_admin)
def add_research(request):
    keyword = Keyword.objects.all()
    author = EndUser.objects.all()
    program = Program.objects.all()
    if request.method == 'POST':
        form = AddResearchForm(request.POST, request.FILES)
        if form.is_valid():
            request.POST.getlist('author')
            request.POST.getlist('keyword')
            program = form.cleaned_data.get('program')
            form.save()
            messages.success(request, ("Research successfully saved."))
            return redirect("reports:add_research")
    else:
        form = AddResearchForm()
    context = {
        "form": form,
        "author": author,
        "keyword": keyword,
        "program": program,
    }
    return render(request, "admin/dashboard/add_research.html", context)

#right nav view
@user_passes_test(check_admin)
def right(request):
    log_his = LoginHistory.objects.all()

    context = {
        "log_his": log_his,
    }
    return render(request, "dashboards/right.html", context)

#edit profile view
@user_passes_test(check_admin)
def edit_profile(request):
    log_his = LoginHistory.objects.all()
    admin = EndUser.objects.get(user=request.user)
    form = EditEndUserForm(instance=admin)
    if request.method == 'POST':
        form = EditEndUserForm(request.POST, request.FILES, instance=admin)
        if form.is_valid():
            form.save()
            messages.success(request, ("Profile edit saved."))
            return redirect("reports:edit_profile")
        else:
            messages.error(request, ("Profile edit failed."))
            return redirect("reports:edit_profile")
    context = {
        "form": form,
        "log_his": log_his,
    }
    return render(request, "admin/dashboard/edit_profile.html", context)

##          END          ##
###                     ###
#### #####-ADMIN-##### ####
###                     ###
##          END          ##


##            START            ##
###                           ###
#### #####-REPORTS/PDF-##### ####
###                           ###
##            START            ##

#researcher view
@user_passes_test(check_admin)
def researcher(request):
    #res_out = Research.objects.all().order_by('school_year')
    res_out = Research.objects.all().order_by("-school_year_to")
    end_user = EndUser.objects.get(user=request.user, is_active=True)
    user = request.user.enduser.first_name + " " + request.user.enduser.last_name
    date_time = datetime.now()
    context = {
        "res_out": res_out,
        "end_user": end_user,
        "date_time": date_time,
        "user":user,
    }
    return render(request, "admin/table/researcher.html", context)

#faculty view
@user_passes_test(check_admin)
def faculty(request):
    res_out = Research.objects.filter(is_active=True).order_by("-school_year_to")
    ress = EndUser.objects.filter(is_faculty = True)
    end_user = EndUser.objects.get(user=request.user, is_active=True)
    user = request.user.enduser.first_name + " " + request.user.enduser.last_name
    date_time = datetime.now()
    context = {
        "res_out": res_out,
        "end_user": end_user,
        "date_time": date_time,
        "user":user,
        "ress": ress,
    }
    return render(request, "admin/table/faculty.html", context)

#student view
@user_passes_test(check_admin)
def student(request):
    res_out = Research.objects.filter(is_faculty=True, is_active=True).order_by("-school_year_to")
    end_user = EndUser.objects.filter(is_student=True, is_active=True)
    user = request.user.enduser.first_name + " " + request.user.enduser.last_name
    date_time = datetime.now()

    context = {
        "end_user": end_user,
        "date_time": date_time,
        "user": user,
        "res_out": res_out,
    }
    return render(request, "admin/table/student.html", context)

#authors and titles view
@user_passes_test(check_admin)
def authors_titles(request):
    res_out = Research.objects.all().order_by("-school_year_to")
    end_user = EndUser.objects.get(user=request.user, is_active=True)
    user = request.user.enduser.first_name + " " + request.user.enduser.last_name
    date_time = datetime.now()
    context = {
        "res_out": res_out,
        "end_user": end_user,
        "date_time": date_time,
        "user":user,
    }
    return render(request, "admin/table/authors_titles.html", context)

#research outputs view
@user_passes_test(check_admin)
def research_output(request):
    res_out = Research.objects.all().order_by("-school_year_to")
    end_user = EndUser.objects.get(user=request.user)
    user = request.user.enduser.first_name + " " + request.user.enduser.last_name
    date_time = datetime.now()
    context = {
        "res_out": res_out,
        "end_user": end_user,
        "date_time": date_time,
        "user":user,
    }
    return render(request, "admin/table/research_outputs.html", context)

#program view
@user_passes_test(check_admin)
def program(request):
    res_out = Research.objects.all().order_by("school_year_from","school_year_to")
    end_user = EndUser.objects.get(user=request.user, is_active=True)
    user = request.user.enduser.first_name + " " + request.user.enduser.last_name
    date_time = datetime.now()
    context = {
        "res_out": res_out,
        "end_user": end_user,
        "date_time": date_time,
        "user":user,
    }
    return render(request, "admin/table/program.html", context)

#login history view
@user_passes_test(check_admin)
def login_history(request):
    log_his = LoginHistory.objects.all().order_by('login_date')
    end_user = EndUser.objects.get(user=request.user, is_active=True)
    user = request.user.enduser.first_name + " " + request.user.enduser.last_name
    date_time = datetime.now()
    context = {
        "log_his": log_his,
        "end_user": end_user,
        "date_time": date_time,
        "user":user,
    }
    return render(request, "admin/table/login_history.html", context)

##            END              ##
###                           ###
#### #####-REPORTS/PDF-##### ####
###                           ###
##            END              ##



##            START            ##
###                           ###
####  #####-VIEW ACCOUNT-##### ####
###                           ###
##            START            ##
@user_passes_test(check_admin)
def all_users(request):
    end_user = EndUser.objects.all()
    context = {
        "end_user": end_user,
    }
    return render(request, "admin/view/all_users.html", context)

@user_passes_test(check_admin)
def all_student(request):
    end_user = EndUser.objects.filter(is_student=True)
    context = {
        "end_user": end_user,
    }
    return render(request, "admin/view/all_student.html", context)

@user_passes_test(check_admin)
def all_faculty(request):
    end_user = EndUser.objects.filter(is_faculty=True)
    context = {
        "end_user": end_user,
    }
    return render(request, "admin/view/all_faculty.html", context)

@user_passes_test(check_admin)
def all_admin(request):
    end_user = EndUser.objects.filter(is_admin=True)
    context = {
        "end_user": end_user,
    }
    return render(request, "admin/view/all_admin.html", context)

##            END            ##
###                           ###
####  #####-VIEW ACCOUNT-##### ####
###                           ###
##            END            ##



##            START            ##
###                           ###
####  #####-IMPORT/CSV-##### ####
###                           ###
##            START            ##

#student
def import_student_csv(request):
    if request.method == 'GET':
        return render(request, "admin/dashboard/student_csv.html")

    csv_file = request.FILES['csvfile']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Please upload a csv file.')
    else:
        EndUser.objects.filter(is_student=True).update(is_active=False)
        data_set = csv_file.read().decode('ISO-8859-1')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=','):

            if EndUser.objects.filter(user__username=column[1], is_student=False, is_faculty=True):
                messages.error(request, " Some accounts in CSV file was already registered as faculty.")
                continue

            elif EndUser.objects.filter(user__username=column[1], is_faculty=False, is_student=True):
                user_check = EndUser.objects.get(user__username=column[1], is_faculty=False, is_student=True)
                user_check.is_active=True
                user_check.save()

            else:
                user = User.objects.create_user(column[1], 'N/A', column[3])
                program = Program.objects.get(name=column[0])
                value = EndUser.objects.create(
                    id=None,
                    user=user,
                    program=program,
                    id_number=column[1],
                    first_name=column[2],
                    last_name=column[3],
                    is_admin=False,
                    is_faculty=False,
                    is_student=True,
                    is_active=True,
                )
            messages.success(request, ("CSV file for Student successfully registered."))
            
    context = {
        'students': EndUser.objects.filter(is_student=True, is_active=True)
    }
    return render(request, "admin/dashboard/student_csv.html", context)

#faculty
def import_faculty_csv(request):
    if request.method == 'GET':
        return render(request, "admin/dashboard/faculty_csv.html")

    csv_file = request.FILES['csvfile']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Please upload a csv file.')

    else: 
        EndUser.objects.filter(is_faculty=True).update(is_active=False)
        data_set = csv_file.read().decode('ISO-8859-1')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=','):

            if EndUser.objects.filter(user__username=column[1], is_student=True, is_faculty=False):
                messages.error(request, " Some acounts in CSV file was already registered as student.")
                continue
         
            elif EndUser.objects.filter(user__username=column[1], is_faculty=True, is_student=False):
                user_check = EndUser.objects.get(user__username=column[1], is_faculty=True)
                user_check.is_active=True
                user_check.save()
            else:
                user = User.objects.create_user(column[1], 'N/A', column[3])
                program = Program.objects.get(name=column[0])
                value = EndUser.objects.create(
                    id=None,
                    user=user,
                    program=program,
                    id_number=column[1],
                    first_name=column[2],
                    last_name=column[3],
                    is_admin=False,
                    is_faculty=True,
                    is_student=False,
                    is_active=True,
                )
            messages.success(request, ("CSV file for Faculty successfully registered."))
    context = {
        'faculties': EndUser.objects.filter(is_faculty=True, is_active=True)
    }
    return render(request, "admin/dashboard/faculty_csv.html", context)
   
#keyword
def import_keyword_csv(request):
    if request.method == 'GET':
        return render(request, "admin/dashboard/keyword_csv.html")

    csv_file = request.FILES['csvfile']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Please upload a csv file.')
        return redirect("reports:import_keyword_csv")
    else :
        data_set = csv_file.read().decode('ISO-8859-1')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=','):
            if column[0] == " " or "":
                    continue
            _, created = Keyword.objects.update_or_create(
                keyword_name=column[0], 
            )
    messages.success(request, ("CSV file for Keywords successfully saved."))
    context = {
        'keywords': Keyword.objects.all()
    }
    return render(request, "admin/dashboard/keyword_csv.html", context)

##            END             ##
###                          ###
#### #####-IMPORT/CSV-##### ####
###                          ###
##            END             ##


##            START             ##
###                          ###
#### #####-LOGIN/REGISTER-##### ####
###                          ###
##            START             ##
def add_admin(request):
    form = AddAdminForm()
    if request.method == "POST":
        form = AddAdminForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data.get('id_number')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            
            if User.objects.filter(username = id_number).first():
                messages.error(request, ("Account is already registered."))
                return redirect("/add_admin")

            user = User.objects.create_user(id_number, 'N/A', last_name, is_superuser=True, is_staff=True)
            enduser = EndUser(
                user=user,
                id_number=id_number,
                first_name=first_name,
                last_name=last_name,
                is_admin=True,
                is_faculty=False,
                is_student=False,
                is_active=True,
            )
            user = enduser.save()
            messages.success(request, ("Account successfully saved."))
            return redirect("/add_admin")
    context = {
        "form": form,
    }
    return render(request, "admin/register/add_admin.html", context)

def add_faculty(request):
    form = AddStudentFacultyForm()
    if request.method == "POST":
        form = AddStudentFacultyForm(request.POST)
        
        if form.is_valid():
            program = form.cleaned_data.get('program')
            id_number = form.cleaned_data.get('id_number')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            prog = Program.objects.get(name=program)
            if User.objects.filter(username = id_number).first():
                messages.error(request, ("Account is already registered."))
                return redirect("/add_faculty")
            user = User.objects.create_user(id_number, 'N/A', last_name)
            enduser = EndUser(
                user=user,
                program=prog,
                id_number=id_number,
                first_name=first_name,
                last_name=last_name,
                is_admin=False,
                is_faculty=True,
                is_student=False,
                is_active=True,
            )
            user = enduser.save()
            messages.success(request, ("Account successfully saved."))
            return redirect("/add_faculty")
    context = {
        "form": form,
    }
    return render(request, "admin/register/add_faculty.html", context)

def add_student(request):
    form = AddStudentFacultyForm()
    if request.method == "POST":
        form = AddStudentFacultyForm(request.POST)
        
        if form.is_valid():
            id_number = form.cleaned_data.get('id_number')
            program = form.cleaned_data.get('program')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            prog = Program.objects.get(name=program)
            if User.objects.filter(username = id_number).first():
                messages.error(request, ("Account is already registered."))
                return redirect("/add_student")
            user = User.objects.create_user(id_number, 'N/A', last_name)
            enduser = EndUser(
                user=user,
                program=prog,
                id_number=id_number,
                first_name=first_name,
                last_name=last_name,
                is_admin=False,
                is_faculty=False,
                is_student=True,
                is_active=True,
            )
            user = enduser.save()
            messages.success(request, ("Account successfully registered."))
            return redirect("/add_student")
    context = {
        "form": form,
    }
    return render(request, "admin/register/add_student.html", context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            end_users = EndUser.objects.get(user=user)
            LoginHistory.objects.create(end_user=end_users)
            if end_users.is_active == False:
                messages.error(request, ("Please enter a correct username and password. Note that both fields may be case-sensitive."))
                return redirect("/login")
            elif end_users.is_active == True:
                if end_users.is_admin == True:
                    return redirect("/dashboard")
                elif end_users.is_student == True or end_users.is_faculty == True:
                    return redirect("/home")
        else:
            messages.error(request, ("Please enter a correct username and password. Note that both fields may be case-sensitive."))
            return redirect("/login")
    else:
        return render(request, "admin/register/login.html", {})

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        forgot_pass = User.objects.filter(username=username).first()

        if not forgot_pass:
            messages.error(request, " Incorrect username.")
            return redirect("/forgot_password")
        
        if forgot_pass:
            forgot_pass1 = User.objects.filter(username=username).first()
            end = EndUser.objects.filter(id_number=username).first()
            forgot_pass1.set_password(end.last_name)
            forgot_pass1.save()
        messages.success(request, "Password was reset. Please, login with your username and default password.")
        return redirect("/login")
    return render(request, "admin/register/forgot_password.html", {})

def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        current_password = request.POST.get('current_password')

        change_pass = request.user
        user = authenticate(change_pass.password)

        if new_password != confirm_password:
            messages.error(request, "The new password and confirm new password didn't match.")

        if not user != current_password:
            messages.error(request, "Incorrect current password.")
        else:
            change_pass.set_password(new_password)
            change_pass.save()
            logout(request)
            messages.success(request, "Password changed. Please, login with your username and new password.")
            return redirect("/login")
    
    return render(request, "admin/register/change_old_password.html")
##            END             ##
###                          ###
#### #####-LOGIN/REGISTER-##### ####
###                          ###
##            END             ##