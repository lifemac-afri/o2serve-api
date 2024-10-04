from django.contrib import admin
from .models import Category, MenuItem

class CategoryAdmin(admin.ModelAdmin):
    # Display specific fields in the list view
    list_display = ('category_name', 'description', 'created_at', 'updated_at')
    
    # Allow search by category name
    search_fields = ('category_name',)
    
    # Add filtering options
    list_filter = ('created_at', 'updated_at')

    # Actions to delete selected categories
    actions = ['delete_selected_categories']

    def delete_selected_categories(self, request, queryset):
        # Custom action to delete selected categories
        queryset.delete()
        self.message_user(request, "Selected categories were deleted successfully.")
    
    delete_selected_categories.short_description = "Delete selected categories"

class MenuItemAdmin(admin.ModelAdmin):
    # Display specific fields in the list view
    list_display = ('item_name', 'category', 'price', 'availability', 'event', 'created_at', 'updated_at')
    
    # Enable filtering by availability, event status, and category
    list_filter = ('availability', 'event', 'category', 'created_at')
    
    # Allow search by item name and category name
    search_fields = ('item_name', 'category__category_name')
    
    # Add actions for bulk management of menu items
    actions = ['mark_as_available', 'mark_as_unavailable', 'delete_selected_menu_items']

    def mark_as_available(self, request, queryset):
        # Mark selected menu items as available
        queryset.update(availability=True)
        self.message_user(request, "Selected items were marked as available.")
    
    def mark_as_unavailable(self, request, queryset):
        # Mark selected menu items as unavailable
        queryset.update(availability=False)
        self.message_user(request, "Selected items were marked as unavailable.")
    
    def delete_selected_menu_items(self, request, queryset):
        # Custom action to delete selected menu items
        queryset.delete()
        self.message_user(request, "Selected menu items were deleted successfully.")

    mark_as_available.short_description = "Mark selected items as available"
    mark_as_unavailable.short_description = "Mark selected items as unavailable"
    delete_selected_menu_items.short_description = "Delete selected menu items"

# Register the admin classes with their models
admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
