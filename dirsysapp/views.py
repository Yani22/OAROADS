from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from datetime import datetime
from xhtml2pdf import pisa
from .resources import *
from .models import *
from .forms import *
import os
import csv

import io

#admin user check
def check_admin(user):
   return user.is_superuser


#home view
def home(request):
    res_out = Research.objects.all()
    end_users = EndUser.objects.filter(is_active=True)
    context = {
        "res_out": res_out,
        "end_users":end_users
    }
    return render(request, "all/home.html", context)

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
    faculty = EndUser.objects.filter(is_faculty=True)
    student = EndUser.objects.filter(is_student=True)
    res_out = Research.objects.all()
    total_faculty = faculty.count()
    total_student = student.count()
    total_res_out = res_out.count()

    context = {
        "end_users": end_users,
        "total_faculty": total_faculty,
        "total_student": total_student,
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
            form.save()
            messages.success(request, ("Keyword successfully saved."))
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
    if request.method == 'POST':
        form = AddResearchForm(request.POST, request.FILES)
        if form.is_valid():
            request.POST.getlist('author')
            form.save()
            messages.success(request, ("Research successfully saved."))
    else:
        form = AddResearchForm()
    context = {
        "form": form,
        "author": author,
        "keyword": keyword,
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

#link_callback parameter
def link_callback(uri, rel):
    """Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources"""
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
            result = list(os.path.realpath(path) for path in result)
            path=result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
           return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
    return path

#researcher view
@user_passes_test(check_admin)
def researcher(request):
    res_out = Research.objects.all()
    context = {
        "res_out": res_out,
    }
    return render(request, "admin/table/researcher.html", context)

#researcher table
@user_passes_test(check_admin)
def reports_researcher(request):
    res_out = Research.objects.all()
    user = request.user.enduser.first_name + " " + request.user.enduser.middle_name + " " + request.user.enduser.last_name + " " + request.user.enduser.suffix_name
    date_time = datetime.now()
    date_user =  "Generated by: " + user + "\n" + "Date and time: " + str(date_time)
    
        # Here is the template you want to convert
    template_path = 'admin/report/researcher_table.html' 
    context = {
        'res_out': res_out,
        'date_user':date_user
    }

        # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="RESEARCHER_REPORT.pdf"'

        # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

        # create a pdf
    pisaStatus = pisa.CreatePDF(
      html, dest=response, link_callback=link_callback)
        # if error then show some funy view
    if pisaStatus.err:
      return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#faculty view
@user_passes_test(check_admin)
def faculty(request):
    res_out = Research.objects.all()
    context = {
        "res_out": res_out,
    }
    return render(request, "admin/table/faculty.html", context)

#faculty table
def reports_faculty(request):
    res_out = Research.objects.all()
    user = request.user.enduser.first_name + " " + request.user.enduser.middle_name + " " + request.user.enduser.last_name + " " + request.user.enduser.suffix_name
    date_time = datetime.now()
    date_user =  "Generated by: " + user + "\n" + "Date and time: " + str(date_time)

    template_path = 'admin/report/faculty_table.html'
    context = {
        'res_out': res_out,
        'date_user':date_user
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="FACULTY_REPORT.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(
      html, dest=response, link_callback=link_callback)
      
    if pisaStatus.err:
      return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#student view
@user_passes_test(check_admin)
def student(request):
    res_out = Research.objects.all()
    context = {
        "res_out": res_out,
    }
    return render(request, "admin/table/student.html", context)

#student table
def reports_student(request):
    res_out = Research.objects.all()
    user = request.user.enduser.first_name + " " + request.user.enduser.middle_name + " " + request.user.enduser.last_name + " " + request.user.enduser.suffix_name
    date_time = datetime.now()
    date_user =  "Generated by: " + user + "\n" + "Date and time: " + str(date_time)

    template_path = 'admin/report/student_table.html'
    context = {
        'res_out': res_out,
        'date_user':date_user
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="STUDENT_REPORT.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(
      html, dest=response, link_callback=link_callback)

    if pisaStatus.err:
      return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#authors and titles view
@user_passes_test(check_admin)
def authors_titles(request):
    res_out = Research.objects.all()
    context = {
        "res_out": res_out,
    }
    return render(request, "admin/table/authors_titles.html", context)

#authors and titles table
def reports_author_title(request):
    res_out = Research.objects.all()
    user = request.user.enduser.first_name + " " + request.user.enduser.middle_name + " " + request.user.enduser.last_name + " " + request.user.enduser.suffix_name
    date_time = datetime.now()
    date_user =  "Generated by: " + user + "\n" + "Date and time: " + str(date_time)

    template_path = 'admin/report/authors_titles_table.html'
    context = {
        'res_out': res_out,
        'date_user':date_user
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="AUTHOR_TITLE_REPORT.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(
      html, dest=response, link_callback=link_callback)

    if pisaStatus.err:
      return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#research outputs view
@user_passes_test(check_admin)
def research_output(request):
    res_out = Research.objects.all()
    context = {
        "res_out": res_out,
    }
    return render(request, "admin/table/research_outputs.html", context)

#research outputs table
def reports_research_output(request):
    res_out = Research.objects.all()
    user = request.user.enduser.first_name + " " + request.user.enduser.middle_name + " " + request.user.enduser.last_name + " " + request.user.enduser.suffix_name
    date_time = datetime.now()
    date_user =  "Generated by: " + user + "\n" + "Date and time: " + str(date_time)
    
    template_path = 'admin/report/research_outputs_table.html'
    context = {
        'res_out': res_out,
        'date_user':date_user
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="RESEARCH_OUTPUT_REPORT.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(
      html, dest=response, link_callback=link_callback)

    if pisaStatus.err:
      return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#program view
@user_passes_test(check_admin)
def program(request):
    res_out = Research.objects.all()
    context = {
        "res_out": res_out,
    }
    return render(request, "admin/table/program.html", context)

#program table
def reports_program(request):
    res_out = Research.objects.all()
    user = request.user.enduser.first_name + " " + request.user.enduser.middle_name + " " + request.user.enduser.last_name + " " + request.user.enduser.suffix_name
    date_time = datetime.now()
    date_user =  "Generated by: " + user + "\n" + "Date and time: " + str(date_time)

    template_path = 'admin/report/program_table.html'
    context = {
        'res_out': res_out,
        'date_user':date_user
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PROGRAM_REPORT.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(
      html, dest=response, link_callback=link_callback)

    if pisaStatus.err:
      return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#login history view
@user_passes_test(check_admin)
def login_history(request):
    log_his = LoginHistory.objects.all()

    context = {
        "log_his": log_his,
    }
    return render(request, "admin/table/login_history.html", context)

#login history table
def reports_login_history(request):
    log_his = LoginHistory.objects.all()
    user = request.user.enduser.first_name + " " + request.user.enduser.middle_name + " " + request.user.enduser.last_name + " " + request.user.enduser.suffix_name
    date_time = datetime.now()
    date_user =  "Generated by: " + user + "\n" + "Date and time: " + str(date_time)

    template_path = 'admin/report/login_history_table.html'  # Here is the template you want to convert
    context = {
        'log_his': log_his,
        'date_user':date_user
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="LOGIN_HISTORY_REPORT.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisaStatus = pisa.CreatePDF(
      html, dest=response, link_callback=link_callback)

    if pisaStatus.err:
      return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

##            END              ##
###                           ###
#### #####-REPORTS/PDF-##### ####
###                           ###
##            END              ##













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
            if column[3] == "" or " ":
                continue
            elif EndUser.objects.filter(user__username=column[3]):
                user_check = EndUser.objects.get(user__username=column[3])
                user_check.is_active=True
                user_check.save()
            else:
                user = User.objects.create_user(column[3], 'N/A', "12345")
                program = Program.objects.get(name=column[0])
                value = EndUser.objects.create(
                    id=None,
                    user=user,
                    program=program,
                    first_name=column[1],
                    middle_name=column[2],
                    last_name=column[3],
                    suffix_name=column[4],
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

    EndUser.objects.filter(is_faculty=True).update(is_active=False)
    data_set = csv_file.read().decode('ISO-8859-1')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=','):
        if column[3] == "" or " ":
                continue
        elif EndUser.objects.filter(user__username=column[3]):
            user_check = EndUser.objects.get(user__username=column[3])
            user_check.is_active=True
            user_check.save()
        else:   
            user = User.objects.create_user(column[3], 'N/A', "12345")
            program = Program.objects.get(name=column[0])
            value = EndUser.objects.create(
                id=None,
                user=user,
                program=program,
                first_name=column[1],
                middle_name=column[2],
                last_name=column[3],
                suffix_name=column[4],
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
    print(Keyword.objects.all())
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
            first_name = form.cleaned_data.get('first_name')
            middle_name = form.cleaned_data.get('middle_name')
            last_name = form.cleaned_data.get('last_name')
            suffix_name = form.cleaned_data.get('suffix_name')
            
            if User.objects.filter(username = last_name).first():
                messages.error(request, first_name + " is already taken.")
                return redirect("/add_user")

            user = User.objects.create_user(last_name, 'N/A', '12345', is_superuser=True, is_staff=True)
            enduser = EndUser(
                user=user,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                suffix_name=suffix_name,
                is_admin=True,
                is_faculty=False,
                is_student=False,
                is_active=True,
            )
            user = enduser.save()
            messages.success(request, (last_name + "'s admin account successfully saved."))
            return redirect("/researcher")
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
            first_name = form.cleaned_data.get('first_name')
            middle_name = form.cleaned_data.get('middle_name')
            last_name = form.cleaned_data.get('last_name')
            suffix_name = form.cleaned_data.get('suffix_name')
            prog = Program.objects.get(name=program)
            if User.objects.filter(username = last_name).first():
                messages.error(request, first_name + " is already taken.")
                return redirect("/add_faculty")
            user = User.objects.create_user(last_name, 'N/A', '12345')
            enduser = EndUser(
                user=user,
                program=prog,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                suffix_name=suffix_name,
                is_admin=False,
                is_faculty=True,
                is_student=False,
                is_active=True,
            )
            user = enduser.save()
            messages.success(request, (last_name + "'s faculty account successfully saved."))
            return redirect("/researcher")
    context = {
        "form": form,
    }
    return render(request, "admin/register/add_faculty.html", context)

def add_student(request):
    form = AddStudentFacultyForm()
    if request.method == "POST":
        form = AddStudentFacultyForm(request.POST)
        
        if form.is_valid():
            program = form.cleaned_data.get('program')
            first_name = form.cleaned_data.get('first_name')
            middle_name = form.cleaned_data.get('middle_name')
            last_name = form.cleaned_data.get('last_name')
            suffix_name = form.cleaned_data.get('suffix_name')
            prog = Program.objects.get(name=program)
            if User.objects.filter(username = last_name).first():
                messages.error(request, first_name + " is already taken.")
                return redirect("/add_student")
            user = User.objects.create_user(last_name, 'N/A', '12345')
            enduser = EndUser(
                user=user,
                program=prog,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                suffix_name=suffix_name,
                is_admin=False,
                is_faculty=False,
                is_student=True,
                is_active=True,
            )
            user = enduser.save()
            messages.success(request, (last_name + "'s student account successfully saved."))
            return redirect("/researcher")
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
                messages.error(request, ("Account deactivated."))
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
        return render(request, "register/login.html", {})
##            END             ##
###                          ###
#### #####-LOGIN/REGISTER-##### ####
###                          ###
##            END             ##






