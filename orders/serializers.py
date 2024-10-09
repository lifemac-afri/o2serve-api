from rest_framework import serializers
from .models import Order, OrderItem
from tables.models import Table
from customers.models import Customer
from menu.models import MenuItem
from authentication.models import User
from notifications_service.notify import notify_order_accepted,notify_order_assigned,notify_order_updated
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
    accepted_status = serializers.BooleanField(required=False)  # New field for acceptance status
    assigned_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)  # New field for assigned user

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'table_number', 'customer_name', 'status', 'total_amount', 'order_date', 'items', 'accepted_status', 'assigned_user']

    def get_table_number(self, obj):
        return obj.table.table_number

    def get_customer_name(self, obj):
        return f"{obj.customer.name}"

    def update(self, instance, validated_data):
        accepted_status = validated_data.get('accepted_status', instance.accepted_status)
        assigned_user = validated_data.get('assigned_user', instance.assigned_user)

        if not instance.accepted_status and accepted_status:
            notify_order_accepted(order_id=instance.order_number)

        if assigned_user and instance.assigned_user != assigned_user:
            notify_order_assigned(order_id=instance.order_number, assignee= instance.assigned_user)

        instance.accepted_status = accepted_status
        instance.assigned_user = assigned_user

        instance.save()
        return instance


class OrderItemCreateSerializer(serializers.ModelSerializer):
    item_id = serializers.UUIDField(write_only=True)  # Accepts UUID for the menu item

    class Meta:
        model = OrderItem
        fields = ['item_id', 'quantity'] 

    def create(self, validated_data):
        # Replace `item_id` with the actual `menu_item`
        menu_item = MenuItem.objects.get(id=validated_data.pop('item_id'))
        order_item = OrderItem.objects.create(menu_item=menu_item, **validated_data)
        return order_item
        
class OrderCreateSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(write_only=True)  
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())  # Accept customer ID
    items = OrderItemCreateSerializer(many=True)  # Accept list of items

    class Meta:
        model = Order
        fields = ['customer', 'status', 'table_number', 'items']  # Include items

    def create(self, validated_data):
        # Extract the table number and retrieve the Table object
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
            # Debugging statement to check the item data structure
            print(f"Processing item: {item_data}")

            # Ensure 'quantity' and 'item_id' are present
            if 'quantity' not in item_data:
                raise serializers.ValidationError("'quantity' field is missing for one of the items.")
            if 'item_id' not in item_data:
                raise serializers.ValidationError("'item_id' field is missing for one of the items.")
                
            OrderItem.objects.create(
                order=order,
                menu_item_id=item_data['item_id'],  # Use item_id directly here
                quantity=item_data['quantity']
            )

        return order

    table_number = serializers.IntegerField(write_only=True)  # Accept table_number from frontend
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())  # Accept customer ID
    items = OrderItemCreateSerializer(many=True)  # Accept list of items

    class Meta:
        model = Order
        fields = ['customer', 'status', 'table_number', 'items']  # Include items

    def create(self, validated_data):
        # Extract the table number and retrieve the Table object
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
            print(f"this item was sent {item_data['item_id']}")
            OrderItem.objects.create(order=order, menu_item_id=item_data['item_id'], quantity=item_data['quantity'])

        return order