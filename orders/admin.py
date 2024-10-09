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
            item.menu_item_price = item.menu_item.price 
            item.subtotal = item.menu_item.price * item.quantity  
        return qs

    def menu_item_price(self, obj):
        return obj.menu_item.price 
    def subtotal(self, obj):
        return obj.menu_item.price * obj.quantity 

class OrderAdmin(admin.ModelAdmin):

    list_display = ('order_number', 'table', 'customer', 'status', 'total_amount','assigned_waiter', 'created_at')
  
    search_fields = ('order_number', 'table')

    list_filter = ['created_at']
    
    def assigned_waiter(self, obj):
        if obj.assigned_user:
            return obj.assigned_user.username  # Return the username instead of ID
        return "No waiter assigned"  # In case no user is assigned
    assigned_waiter.short_description = 'Assigned Waiter'
    
    inlines = [OrderItemInline]  

admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)