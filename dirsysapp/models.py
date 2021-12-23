
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models

# Create your models here.
class Program(models.Model):
    PROGRAM_TYPE_CHOICES = [
        ('Programs', 
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
    
    name = models.CharField(max_length=31, choices=PROGRAM_TYPE_CHOICES, blank=True, null=True)
    logo = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return self.name

class EndUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    suffix_name = models.CharField(max_length=100, blank=True, null=True)
    is_admin = models.BooleanField(default=True)
    profile = models.ImageField(upload_to='images/', null=True)
    is_faculty = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + self.last_name

class Keyword(models.Model):
    keyword_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.keyword_name

class Research(models.Model):
    title = models.CharField(max_length=100)
    keyword = models.ManyToManyField(Keyword)
    author = models.ManyToManyField(EndUser)
    pdf = models.FileField(upload_to='documents/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True)
    school_year = models.DateField(default=datetime.now().year)

    def __str__(self):
        return self.title

class LoginHistory(models.Model):
    end_user = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    login_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.end_user.first_name + " " + self.end_user.last_name
        