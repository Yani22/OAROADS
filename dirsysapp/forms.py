from django import forms
from .models import *

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
            ('AB ENG.', 'Liberal Arts Program (AB ENG.)'),
            ('AB PSYCH.', 'Liberal Arts Program (AB PSYCH.)'),
        )
    ),
]
class AddKeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ("keyword_name",)

class AddResearchForm(forms.ModelForm):
    program = forms.ChoiceField(choices=PROGRAM_TYPE_CHOICES, required=True)
    class Meta:
        model = Research
        fields = ("program", "title", "keyword", "author", "pdf", "school_year_from", "school_year_to")

class EditEndUserForm(forms.ModelForm):
    class Meta:
        model = EndUser
        fields = ("profile", "first_name", "last_name")
        exclude = ['user',]

        labels = {
            "profile":"",
            "first_name":"",
            "last_name":"",
            }

class EditUserForm(forms.ModelForm):
    class Meta:
        model = EndUser
        fields = ("profile", "first_name", "last_name")
        exclude = ['user',]

        labels = {
            "profile":"",
            "first_name":"",
            "last_name":"",
        }

class AddAdminForm(forms.Form):
    id_number = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

class AddStudentFacultyForm(forms.Form):
    id_number = forms.CharField(required=True)
    program = forms.ChoiceField(choices=PROGRAM_TYPE_CHOICES, required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)