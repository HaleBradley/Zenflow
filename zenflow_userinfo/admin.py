from django.contrib import admin
from zenflow_userinfo.models import Team, Employee

# Register your models here.
admin.site.register(Team)
admin.site.register(Employee)