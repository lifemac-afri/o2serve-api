from rest_framework import serializers
from .models import Order, OrderItem
from tables.models import Table
from customers.models import Customer
from menu.models import MenuItem

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['menu_item_name', 'quantity']

    def get_menu_item_name(self, obj):
        return obj.menu_item.item_name

class OrderSerializer(serializers.ModelSerializer):
    table_number = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'table_number', 'customer_name', 'status', 'total_amount', 'order_date', 'items']

    def get_table_number(self, obj):
        return obj.table.table_number

    def get_customer_name(self, obj):
        return f"{obj.customer.name}"

class OrderCreateSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(write_only=True)  # Accept table_number from the frontend
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())  # Expect customer ID

    class Meta:
        model = Order
        fields = ['customer', 'status', 'table_number']  # Include table_number instead of table

    def create(self, validated_data):
        # Extract table_number and retrieve the Table object
        table_number = validated_data.pop('table_number')
        try:
            table = Table.objects.get(table_number=table_number)
        except Table.DoesNotExist:
            raise serializers.ValidationError(f"Table with number {table_number} does not exist.")

        # Create the order with the table and the rest of the validated data
        order = Order.objects.create(table=table, **validated_data)
        return order

    table_number = serializers.IntegerField(write_only=True)  

    class Meta:
        model = Order
        fields = ['customer', 'status', 'table_number']  

    def create(self, validated_data):
        
        table_number = validated_data.pop('table_number')
        customer_id = validated_data.pop('customer')

        print(f"customer id is :{customer_id}")
        
        try:
            table = Table.objects.get(table_number=table_number)
            customer = Customer.objects.get(phone_number=customer_id)
        except Table.DoesNotExist:
            raise serializers.ValidationError(f"Table with number {table_number} does not exist.")

       
        order = Order.objects.create(table=table, customer=customer, **validated_data)
        return order
    

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