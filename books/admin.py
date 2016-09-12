from django.contrib import admin
from books.models import *


# Register your models here.

class ResAdmin(admin.ModelAdmin):

    list_display = ('companyShortName', 'companySize', 'positionName', 'salary', 'positionAdvantage', 'workYear','education','createTime')

admin.site.register(Result, ResAdmin)

