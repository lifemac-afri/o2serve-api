from rest_framework import serializers
from .models import Order, OrderItem
from tables.models import Table
from customers.models import Customer
from menu.models import MenuItem
from authentication.models import User
from notifications_service.notify import notify_order_assigned,notify_order_updated
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.SerializerMethodField()
    menu_item_price = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()  # Add subtotal field

    class Meta:
        model = OrderItem 
        fields = ['menu_item_name', 'quantity', 'menu_item_price', 'subtotal']  # Include subtotal in fields

    def get_menu_item_name(self, obj):
        return obj.menu_item.item_name
    
    def get_menu_item_price(self, obj):
        return obj.menu_item.price

    def get_subtotal(self, obj):
        return obj.menu_item.price * obj.quantity  

class OrderSerializer(serializers.ModelSerializer):
    table_number = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    accepted_status = serializers.BooleanField(required=False)
    assigned_waiter = serializers.SerializerMethodField()
    served = serializers.BooleanField()
    id = serializers.UUIDField(format='hex')

    class Meta:
        model = Order
        fields = [
            'id', 
            'order_number', 
            'table_number', 
            'customer_name', 
            'status', 
            'total_amount', 
            'order_date', 
            'items', 
            'accepted_status', 
            'assigned_waiter', 
            'served'
        ]

    def get_table_number(self, obj):
        return obj.table.table_number if obj.table else None

    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else None
    
    def get_assigned_waiter(self, obj):
        return obj.assigned_waiter.username if obj.assigned_waiter else None

    def to_representation(self, instance):
        try:
            return super().to_representation(instance)
        except Exception as e:
            raise serializers.ValidationError(f"Error serializing order: {str(e)}")

class OrderItemCreateSerializer(serializers.ModelSerializer):
    item_id = serializers.UUIDField(write_only=True)  # Accepts UUID for the menu item

    class Meta:
        model = OrderItem
        fields = ['item_id', 'quantity'] 

    def create(self, validated_data):
        menu_item = MenuItem.objects.get(id=validated_data.pop('item_id'))
        order_item = OrderItem.objects.create(menu_item=menu_item, **validated_data)
        return order_item
        
class OrderCreateSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(write_only=True)  
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())  
    items = OrderItemCreateSerializer(many=True)  

    class Meta:
        model = Order
        fields = ['customer', 'status', 'table_number', 'items']  # Include items

    def create(self, validated_data):
        
        table_number = validated_data.pop('table_number')
        items_data = validated_data.pop('items')  # Extract items data
        
        try:
            table = Table.objects.get(table_number=table_number)           
        except Table.DoesNotExist:
            raise serializers.ValidationError(f"Table with number {table_number} does not exist.")

        # Create the order
        order = Order.objects.create(table=table, **validated_data)
        # Create the OrderItem records for the order
        for item_data in items_data:
            # Ensure 'quantity' and 'item_id' are present
            if 'quantity' not in item_data:
                raise serializers.ValidationError("'quantity' field is missing for one of the items.")
            if 'item_id' not in item_data:
                raise serializers.ValidationError("'item_id' field is missing for one of the items.")
                
            # Retrieve the menu item and reduce its quantity
            menu_item = MenuItem.objects.get(id=item_data['item_id'])
            if menu_item.quantity < item_data['quantity']:
                raise serializers.ValidationError(f"Insufficient stock for item {menu_item.item_name}.")
            
            # Create the OrderItem
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,  # Use the menu_item object directly
                quantity=item_data['quantity']
            )
            
            # Reduce the quantity of the menu item
            menu_item.quantity -= item_data['quantity']
            menu_item.save()  # Save the updated menu item

        return order

