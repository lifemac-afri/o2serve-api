from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone_number', 'is_verified', 'otp', 'created_at', 'updated_at']
        read_only_fields = ['is_verified', 'otp']

    def create(self, validated_data):
        customer = Customer.objects.create(**validated_data)
        # Generate and send OTP logic here, if required.
        return customer
