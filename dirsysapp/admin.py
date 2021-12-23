from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class BookResource(resources.ModelResource):

    class Meta:
        model = Keyword

# Register your models here.
@admin.register(EndUser)
class EndUserAdmin(ImportExportModelAdmin):
    list_display = ('id','user','program','first_name','last_name',
                    'is_admin','is_faculty','is_student','is_active',)

@admin.register(Keyword)
class KeywordAdmin(ImportExportModelAdmin):
    list_display = ('id','keyword_name',)


admin.site.register(Research)
admin.site.register(LoginHistory)
admin.site.register(Program)