    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user_type = form.cleaned_data.get('user_type')
            program = form.cleaned_data.get('program')
            first_name = form.cleaned_data.get('first_name')
            middle_name = form.cleaned_data.get('middle_name')
            last_name = form.cleaned_data.get('last_name')
            suffix_name = form.cleaned_data.get('suffix_name')
            for prog in Program.objects.filter(name=program):
                if user_type == "Faculty":
                    if User.objects.filter(username = last_name).first():
                        messages.error(request, first_name + " is already taken.")
                        return redirect("/add_user")
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
                    return redirect("/faculty")

                if user_type == "Student":
                    if User.objects.filter(username = last_name).first():
                        messages.error(request, first_name + " is already taken.")
                        return redirect("/add_user")
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
                    return redirect("/student")

                if user_type == "Admin":
                    if User.objects.filter(username = last_name).first():
                        messages.error(request, first_name + " is already taken.")
                        return redirect("/add_user")
                    user = User.objects.create_user(last_name, 'N/A', '12345', is_superuser=True, is_staff=True)
                    enduser = EndUser(
                        user=user,
                        program=prog,
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