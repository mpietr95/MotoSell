from rest_framework import serializers
from .models import Vehicle, VehicleImage


class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ['id', 'image', 'uploaded_at']


class VehicleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    fuel_type_display = serializers.CharField(source='get_fuel_type_display', read_only=True)
    images = VehicleImageSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id', 'title', 'description',
            'category', 'category_display',
            'brand', 'model', 'year', 'mileage',
            'engine_capacity', 'power',
            'fuel_type', 'fuel_type_display',
            'user', 'image', 'images',
            'created_at', 'published_at',
        ]
        read_only_fields = ['id', 'user', 'created_at']
