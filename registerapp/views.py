from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from dirsysapp.models import *



# Create your views here.

def signup(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user_type = form.cleaned_data.get('user_type')
            program = form.cleaned_data.get('program')
            id_number = form.cleaned_data.get('id_number')
            first_name = form.cleaned_data.get('first_name')
            middle_name = form.cleaned_data.get('middle_name')
            last_name = form.cleaned_data.get('last_name')
            suffix_name = form.cleaned_data.get('suffix_name')
            address = form.cleaned_data.get('address')
            for prog in Program.objects.filter(name=program):
                if user_type == "Faculty":
                    user = User.objects.create_user(last_name, 'N/A', 'faculty')
                    enduser = EndUser(
                        user=user,
                        program=prog,
                        id_number="N/A",
                        first_name=first_name,
                        middle_name=middle_name,
                        last_name=last_name,
                        suffix_name=suffix_name,
                        address=address,
                        is_admin=False,
                        is_faculty=True,
                        is_student=False,
                        is_active=True,
                    )
                    user = enduser.save()
                    messages.success(request, ("Faculty account successfully saved."))
                    return redirect("/researcher")

                if user_type == "Student":
                    user = User.objects.create_user(id_number, 'N/A', last_name)
                    enduser = EndUser(
                        user=user,
                        program=prog,
                        id_number=id_number,
                        first_name=first_name,
                        middle_name=middle_name,
                        last_name=last_name,
                        suffix_name=suffix_name,
                        address=address,
                        is_admin=False,
                        is_faculty=False,
                        is_student=True,
                        is_active=True,
                    )
                    user = enduser.save()
                    messages.success(request, ("Student account successfully saved."))
                    return redirect("/researcher")

                if user_type == "Admin":
                    user = User.objects.create_user(last_name, 'N/A', "admin")
                    enduser = EndUser(
                        user=user,
                        program=prog,
                        id_number=id_number,
                        first_name=first_name,
                        middle_name=middle_name,
                        last_name=last_name,
                        suffix_name=suffix_name,
                        address=address,
                        is_admin=True,
                        is_faculty=False,
                        is_student=False,
                        is_active=True,
                    )
                    user = enduser.save()
                    messages.success(request, ("Admin account successfully saved."))
                    return redirect("/researcher")
    context = {
        "form": form,
    }
    return render(request, "register/register.html", context)

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