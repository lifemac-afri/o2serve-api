from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('menu_item', 'quantity', 'menu_item_price', 'subtotal')
    readonly_fields = ('menu_item_price', 'subtotal')

    def menu_item_price(self, obj):
        return obj.menu_item.price
    
    def subtotal(self, obj):
        return obj.menu_item.price * obj.quantity

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'table', 'customer', 'status', 'total_amount', 'assigned_waiter', 'served', 'created_at')
    list_filter = ('status', 'served', 'created_at')
    search_fields = ('order_number', 'table__table_number', 'customer__name', 'assigned_waiter__username')
    readonly_fields = ('order_number', 'total_amount', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    ordering = ['-created_at']
    actions = ['mark_as_completed', 'mark_as_canceled', 'mark_as_served']

    def assigned_waiter(self, obj):
        return obj.assigned_waiter.username if obj.assigned_waiter else "No waiter assigned"
    assigned_waiter.short_description = 'Assigned Waiter'

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected orders as completed"

    def mark_as_canceled(self, request, queryset):
        queryset.update(status='canceled')
    mark_as_canceled.short_description = "Mark selected orders as canceled"

    def mark_as_served(self, request, queryset):
        queryset.update(served=True)
    mark_as_served.short_description = "Mark selected orders as served"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'item_price', 'subtotal')
    list_filter = ('order__status', 'menu_item__category')
    search_fields = ('order__order_number', 'menu_item__item_name')

    def item_price(self, obj):
        return obj.menu_item.price
    item_price.short_description = 'Item Price'

    def subtotal(self, obj):
        return obj.menu_item.price * obj.quantity
    subtotal.short_description = 'Subtotal'
