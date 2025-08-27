from rest_framework import serializers

# Serializer code
class MenuItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    category = serializers.CharField(max_length=50)
    is_vegetarian = serializers.BooleanField()
    is_available = serializers.BooleanField()