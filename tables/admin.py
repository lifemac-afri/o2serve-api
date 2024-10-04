from django.contrib import admin
from .models import Table

class TableAdmin(admin.ModelAdmin):
    # Display specific fields in the list view
    list_display = ('table_number', 'capacity', 'created_at', 'updated_at')
    
    # Enable filtering options by capacity and created date
    list_filter = ('capacity', 'created_at')
    
    # Allow search by table number
    search_fields = ('table_number',)
    
    # Add actions for bulk management
    actions = ['delete_selected_tables']

    def delete_selected_tables(self, request, queryset):
        # Custom action to delete selected tables
        queryset.delete()
        self.message_user(request, "Selected tables were deleted successfully.")
    
    # Set the name of the action in the dropdown
    delete_selected_tables.short_description = "Delete selected tables"

# Register the admin class with the model
admin.site.register(Table, TableAdmin)
