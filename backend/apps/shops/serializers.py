from rest_framework import serializers

class ShopSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # Mongo ObjectId as string
    vendor_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    owner_name = serializers.CharField(max_length=255)
    business_type = serializers.CharField(max_length=100, allow_blank=True, required=False)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    distance_km = serializers.FloatField(read_only=True, required=False)