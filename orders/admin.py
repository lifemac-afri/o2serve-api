from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):  # Use TabularInline for a compact view
    model = OrderItem
    extra = 0  

class OrderAdmin(admin.ModelAdmin):
    # Display specific fields in the list view
    list_display = ('order_number', 'table', 'customer', 'status', 'total_amount', 'created_at')
  
    search_fields = ('order_number', 'table')
    
    # Add filtering options
    list_filter = ['created_at']
    
    # Include the inline for OrderItem
    inlines = [OrderItemInline]  # {{ edit_1 }}

admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)