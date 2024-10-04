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

    class Meta:
        model = Order
        fields = ['customer', 'status', 'table_number']  # Include table_number instead of table

    def create(self, validated_data):
        
        table_number = validated_data.pop('table_number')

        
        try:
            table = Table.objects.get(table_number=table_number)
        except Table.DoesNotExist:
            raise serializers.ValidationError(f"Table with number {table_number} does not exist.")

       
        order = Order.objects.create(table=table, **validated_data)
        return order