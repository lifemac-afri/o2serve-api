from rest_framework import serializers
from .models import MenuItem, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['id', 'item_name', 'description', 'price', 'availability', 'category_name', 'event', 'created_at', 'updated_at']

    def get_category_name(self, obj):
        return obj.category.category_name