from django.contrib import admin
from .models import Customer, ActivityLog

class CustomerAdmin(admin.ModelAdmin):
    # Display specific fields in the list view
    list_display = ('name', 'phone_number', 'is_verified', 'otp', 'created_at', 'updated_at')
    
    # Enable search by name and phone number
    search_fields = ('name', 'phone_number')
    
    # Add filtering options
    list_filter = ('is_verified', 'created_at')
    
    # Add actions for bulk management of customers
    actions = ['verify_customers', 'unverify_customers', 'delete_selected_customers']

    def verify_customers(self, request, queryset):
        # Mark selected customers as verified
        queryset.update(is_verified=True)
        self.message_user(request, "Selected customers were marked as verified.")
    
    def unverify_customers(self, request, queryset):
        # Mark selected customers as unverified
        queryset.update(is_verified=False)
        self.message_user(request, "Selected customers were marked as unverified.")
    
    def delete_selected_customers(self, request, queryset):
        # Custom action to delete selected customers
        queryset.delete()
        self.message_user(request, "Selected customers were deleted successfully.")

    verify_customers.short_description = "Mark selected customers as verified"
    unverify_customers.short_description = "Mark selected customers as unverified"
    delete_selected_customers.short_description = "Delete selected customers"

class ActivityLogAdmin(admin.ModelAdmin):
    # Display specific fields in the list view
    list_display = ('activity', 'created_at')
    
    # Enable search by activity name
    search_fields = ('activity',)
    
    # Add filtering by creation date
    list_filter = ('created_at',)

    # Actions for managing logs
    actions = ['delete_selected_logs']

    def delete_selected_logs(self, request, queryset):
        # Custom action to delete selected activity logs
        queryset.delete()
        self.message_user(request, "Selected activity logs were deleted successfully.")
    
    delete_selected_logs.short_description = "Delete selected logs"

# Register the admin classes with the models
admin.site.register(Customer, CustomerAdmin)
admin.site.register(ActivityLog, ActivityLogAdmin)
