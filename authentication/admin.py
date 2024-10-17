from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Worker

class WorkerInline(admin.StackedInline):
    model = Worker
    can_delete = False
    verbose_name_plural = 'Worker'

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'is_logged_in', 'created_at', 'updated_at')
    list_filter = ('role', 'is_active', 'is_staff', 'is_logged_in', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-updated_at',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Login Status', {'fields': ('is_logged_in',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    inlines = (WorkerInline,)
    actions = ['make_admin', 'make_waiter', 'make_superadmin', 'activate_users', 'deactivate_users']

    def make_admin(self, request, queryset):
        queryset.update(role='admin')
    make_admin.short_description = "Mark selected users as Admin"

    def make_waiter(self, request, queryset):
        queryset.update(role='waiter')
    make_waiter.short_description = "Mark selected users as Waiter"

    def make_superadmin(self, request, queryset):
        queryset.update(role='superadmin')
    make_superadmin.short_description = "Mark selected users as Superadmin"

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Deactivate selected users"

admin.site.register(User, CustomUserAdmin)

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_order_assigned')
    search_fields = ('user__username', 'user__email')
    list_filter = ('last_order_assigned',)
    ordering = ('-last_order_assigned',)
