from .models import Keyword
from import_export import resources
from django.contrib.auth.models import User
from import_export.fields import Field
from .models import *

class EndUserResource(resources.ModelResource):
    class meta:
        model = EndUser
        fields = ["program", "first_name", "last_name"]

class KeywordResource(resources.ModelResource):
    class meta:
        model = Keyword
        fields = ["keyword_name"]