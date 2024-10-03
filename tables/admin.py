from django.contrib import admin

# Register your models here.
from .models import Table
# Register your models here.
admin.site.register([Table])