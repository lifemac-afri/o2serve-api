from django.contrib import admin
from .models import Category, MenuItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'description', 'created_at', 'updated_at')
    search_fields = ('category_name',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['delete_selected_categories']
    ordering = ('-updated_at',)
    def delete_selected_categories(self, request, queryset):
        queryset.delete()
    delete_selected_categories.short_description = "Delete selected categories"

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'category', 'price', 'availability', 'event', 'quantity', 'created_at', 'updated_at')
    list_filter = ('availability', 'event', 'category', 'created_at')
    search_fields = ('item_name', 'category__category_name')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_available', 'mark_as_unavailable', 'mark_as_event', 'mark_as_non_event', 'delete_selected_menu_items']
    ordering = ('-updated_at',)
    def mark_as_available(self, request, queryset):
        queryset.update(availability=True)
    mark_as_available.short_description = "Mark selected items as available"

    def mark_as_unavailable(self, request, queryset):
        queryset.update(availability=False)
    mark_as_unavailable.short_description = "Mark selected items as unavailable"

    def mark_as_event(self, request, queryset):
        queryset.update(event=True)
    mark_as_event.short_description = "Mark selected items as event items"

    def mark_as_non_event(self, request, queryset):
        queryset.update(event=False)
    mark_as_non_event.short_description = "Mark selected items as non-event items"

    def delete_selected_menu_items(self, request, queryset):
        queryset.delete()
    delete_selected_menu_items.short_description = "Delete selected menu items"
