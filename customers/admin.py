from django.contrib import admin
from .models import Customer, ActivityLog

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'is_verified', 'otp', 'created_at', 'updated_at')
    search_fields = ('name', 'phone_number')
    list_filter = ('is_verified', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['verify_customers', 'unverify_customers', 'delete_selected_customers']
    ordering = ('-updated_at',)

    def verify_customers(self, request, queryset):
        queryset.update(is_verified=True)
    verify_customers.short_description = "Mark selected customers as verified"

    def unverify_customers(self, request, queryset):
        queryset.update(is_verified=False)
    unverify_customers.short_description = "Mark selected customers as unverified"

    def delete_selected_customers(self, request, queryset):
        queryset.delete()
    delete_selected_customers.short_description = "Delete selected customers"

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('activity', 'created_at')
    search_fields = ('activity',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
