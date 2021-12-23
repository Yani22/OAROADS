from django.contrib.auth.models import User
from django import forms
from dirsysapp.models import *
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(forms.Form):
    PROGRAM_TYPE_CHOICES = [
        ('Program',
            (
                ('BSN', 'Nursing Program'),
                ('BSHM', 'Hospitality Management Program'),
                ('BSTM', 'Tourism Management Program'),
                ('BSA', 'Accountancy Program'),
                ('AB', 'Liberal Arts Program'),
                ('BS CRIM.', 'Criminology Program'),
                ('BSBA', 'Business Administration Program'),
                ('BSCE', 'Civil Engineering Program'),
                ('BEED', 'Elementary Education Program'),
                ('BSED', 'Secondary Education Program'),
                ('BSCS', 'Computer Science Program'),
                ('J.D.', 'Juris Doctor Program'),
            )
        ),
    ]
    USER_TYPE_CHOICES= [
        ('User Type', 
            (
                ('Admin', 'Admin'),
                ('Faculty', 'Faculty'),
                ('Student', 'Student'),
            )
        ),
    ]
    YEAR_LEVEL_CHOICES= [
        ('Year Level', 
            (
                ('First Year', 'First Year'),
                ('Second Year', 'Second Year'),
                ('Third Year', 'Third Year'),
                ('Fourth Year', 'Fourth Year'),
            )
        ),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)
    program = forms.ChoiceField(choices=PROGRAM_TYPE_CHOICES, required=True)
    id_number = forms.CharField(required=False)
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField(required=True)
    suffix_name = forms.CharField(required=False)
    address = forms.CharField(required=True)