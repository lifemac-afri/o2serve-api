from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Define fields to display in the list view
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'created_at', 'updated_at')
    
    # Enable search by username and email
    search_fields = ('username', 'email')
    
    # Add filtering options for role, active status, and staff status
    list_filter = ('role', 'is_active', 'is_staff', 'created_at')
    
    # Fields that are editable in the admin form
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        
    )
    
    # Add actions for managing users
    actions = ['make_admin', 'make_waiter', 'make_superadmin', 'delete_selected_users']


    def make_admin(self, request, queryset):
        # Mark selected users as Admin
        queryset.update(role='admin')
        self.message_user(request, "Selected users were marked as Admins.")
    
    def make_waiter(self, request, queryset):
        # Mark selected users as Waiters
        queryset.update(role='waiter')
        self.message_user(request, "Selected users were marked as Waiters.")
    
    def make_superadmin(self, request, queryset):
        # Mark selected users as Superadmins
        queryset.update(role='superadmin')
        self.message_user(request, "Selected users were marked as Superadmins.")
    
    def delete_selected_users(self, request, queryset):
        # Custom action to delete selected users
        queryset.delete()
        self.message_user(request, "Selected users were deleted successfully.")

    # Set the name of the actions in the dropdown
    make_admin.short_description = "Mark selected users as Admin"
    make_waiter.short_description = "Mark selected users as Waiter"
    make_superadmin.short_description = "Mark selected users as Superadmin"
    delete_selected_users.short_description = "Delete selected users"

# Register the custom UserAdmin with the model
admin.site.register(User, UserAdmin)
