from django.contrib import admin

from .models import *


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Company._meta.fields]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Employee._meta.fields]
