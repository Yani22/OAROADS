from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models

# Create your models here.
class Program(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ImageField(upload_to='images/', null=True)
    def __str__(self):
        return self.name

class EndUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True, null=True)
    id_number = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    profile = models.ImageField(upload_to='images/', null=True,blank=True)
    is_admin = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + self.last_name

class Keyword(models.Model):
    keyword_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.keyword_name

class PDFtoImages(models.Model):
    to_images = models.ImageField(upload_to='images/', null=True,blank=True)

    def __str__(self):
        return self.to_images.url

class Research(models.Model):
    program = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100)
    keyword = models.ManyToManyField(Keyword)
    author = models.ManyToManyField(EndUser)
    pdf = models.FileField(upload_to='documents/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], null=True)
    from_images = models.ManyToManyField(PDFtoImages, blank=True)
    school_year_from = models.IntegerField(default="1948")
    school_year_to = models.IntegerField(default=datetime.now().year)
    is_faculty = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class LoginHistory(models.Model):
    end_user = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    login_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.end_user.first_name + " " + self.end_user.last_name
        