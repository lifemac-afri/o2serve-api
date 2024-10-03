from django.contrib import admin
from .models import Customer,ActivityLog
# Register your models here.
admin.site.register([Customer,ActivityLog])