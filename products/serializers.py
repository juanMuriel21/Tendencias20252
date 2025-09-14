from rest_framework import serializers

from products.models import Product


class ProductRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    category = serializers.CharField(max_length=100, required=True)
    subcategory = serializers.CharField(max_length=100, required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    quantity = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return Product(**validated_data)

class ProductDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def map_to_entity(self, data) -> Product:
        return Product(**data)