from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    fuel_type_display = serializers.CharField(source='get_fuel_type_display', read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id', 'title', 'description',
            'category', 'category_display',
            'brand', 'model', 'year', 'mileage',
            'engine_capacity', 'power',
            'fuel_type', 'fuel_type_display',
            'user', 'image',
            'created_at', 'published_at',
        ]
        read_only_fields = ['id', 'user', 'created_at']
