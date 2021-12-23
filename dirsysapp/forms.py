from django import forms
from .models import *

class AddKeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ("keyword_name",)

class AddResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = ("title", "keyword", "author", "pdf", "school_year")

class EditEndUserForm(forms.ModelForm):
    class Meta:
        model = EndUser
        fields = '__all__'
        exclude = ['user',]

        labels = {
            "profile":"",
            "first_name":"",
            "middle_name":"",
            "last_name":"",
            "suffix_name":"",
            }

class AddAdminForm(forms.Form):
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField(required=True)
    suffix_name = forms.CharField(required=False)

class AddStudentFacultyForm(forms.Form):
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
    program = forms.ChoiceField(choices=PROGRAM_TYPE_CHOICES, required=True)
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField(required=True)
    suffix_name = forms.CharField(required=False)

