
#from registerapp import views as registerAppViews
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [   
    ### #####-ALL USERS-##### ###
    path('home/', views.home, name="home"),
    path("login/", views.login_user, name="login"),
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
    path('reports_researcher/', views.reports_researcher, name='reports_researcher'),
    path('faculty/', views.faculty, name='faculty'), 
    path('reports_faculty/', views.reports_faculty, name='reports_faculty'),
    path('student/', views.student, name='student'),
    path('reports_student/', views.reports_student, name='reports_student'),
    path('authors_titles/', views.authors_titles, name='authors_titles'),
    path('reports_author_title/', views.reports_author_title, name='reports_author_title'),
    path('research_output/', views.research_output, name='research_output'),
    path('reports_research_output/', views.reports_research_output, name='reports_research_output'),
    path('program/', views.program, name='program'),
    path('reports_program/', views.reports_program, name='reports_program'),
    path('login_history/', views.login_history, name='login_history'),
    path('reports_login_history/', views.reports_login_history, name='reports_login_history'),
    #### #####-REPORTS/PDF-##### ####

    ####  #####-IMPORT/CSV-##### ####
    path('import_student_csv/', views.import_student_csv, name='import_student_csv'),
    path('import_faculty_csv/', views.import_faculty_csv, name='import_faculty_csv'),
    path('import_keyword_csv/', views.import_keyword_csv, name='import_keyword_csv'),
    ####  #####-IMPORT/CSV-##### ####




]