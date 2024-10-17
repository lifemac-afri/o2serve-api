from django.contrib import admin
from .models import Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'created_at', 'updated_at')
    search_fields = ('table_number',)
    list_filter = ('capacity', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'qr_code')
    fields = ('table_number', 'capacity', 'qr_code', 'created_at', 'updated_at')
    ordering = ('-updated_at',)
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('table_number',)
        return self.readonly_fields
