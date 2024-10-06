from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):  # Use TabularInline for a compact view
    model = OrderItem
    extra = 0  
    fields = ('menu_item', 'quantity', 'menu_item_price', 'subtotal')  # Specify fields to display
    readonly_fields = ('menu_item_price', 'subtotal')  # Make price and subtotal read-only

    def get_queryset(self, request):
        # Override to include the price calculation in the queryset
        qs = super().get_queryset(request)
        for item in qs:
            item.menu_item_price = item.menu_item.price  # Add price to the queryset
            item.subtotal = item.menu_item.price * item.quantity  # Calculate subtotal
        return qs

    def menu_item_price(self, obj):
        return obj.menu_item.price  # Display the price of the menu item

    def subtotal(self, obj):
        return obj.menu_item.price * obj.quantity  # Calculate subtotal

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