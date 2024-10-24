from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone_number', 'is_verified', 'otp', 'created_at', 'updated_at']
        read_only_fields = ['is_verified', 'otp']

    def create(self, validated_data):
        customer = Customer.objects.create(**validated_data)
        return customer


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    user_id = serializers.UUIDField()



class CustomerOrderUpdateSerializer(serializers.Serializer):
    id = serializers.CharField()
    served = serializers.BooleanField(required=False)
