
#from registerapp import views as registerAppViews
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [ 
    ### #####-ALL USERS-##### ###
    path('home/', views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("change_password/", views.change_password, name="change_password"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("my_account/", views.my_account, name="my_account"),
    ### #####-ALL USERS-##### ###

    #### #####-ADMIN-##### ####
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path("add_admin/", views.add_admin, name="add_admin"),
    path("add_faculty/", views.add_faculty, name="add_faculty"),
    path("add_student/", views.add_student, name="add_student"),
    path('add_keyword/', views.add_keyword, name="add_keyword"),
    path('add_research/', views.add_research, name="add_research"),
    #### #####-ADMIN-##### ####

    #### #####-REPORTS/PDF-##### ####
    path('researcher/', views.researcher, name='researcher'),
    path('faculty/', views.faculty, name='faculty'),
    path('student/', views.student, name='student'),
    path('authors_titles/', views.authors_titles, name='authors_titles'),
    path('research_output/', views.research_output, name='research_output'),
    path('program/', views.program, name='program'),
    path('login_history/', views.login_history, name='login_history'),
    #### #####-REPORTS/PDF-##### ####

    #### #####-ACCOUNTS/VIEW-##### ####
    path('all_users/', views.all_users, name='all_users'),
    path('all_admin/', views.all_admin, name='all_admin'),
    path('all_faculty/', views.all_faculty, name='all_faculty'),
    path('all_student/', views.all_student, name='all_student'),
    #### #####-ACCOUNTS/VIEW-##### ####

    ####  #####-IMPORT/CSV-##### ####
    path('import_student_csv/', views.import_student_csv, name='import_student_csv'),
    path('import_faculty_csv/', views.import_faculty_csv, name='import_faculty_csv'),
    path('import_keyword_csv/', views.import_keyword_csv, name='import_keyword_csv'),
    ####  #####-IMPORT/CSV-##### ####
]