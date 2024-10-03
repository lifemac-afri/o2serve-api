from rest_framework import serializers
from .models import Table

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'table_number', 'capacity', 'qr_code', 'created_at', 'updated_at']
        read_only_fields = ['qr_code']  # The QR code is auto-generated and should not be manually provided
