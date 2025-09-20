from rest_framework import serializers

from clients.models import Client
from products.models import Product
from transactions.models import Transaction, ProductPerTransaction


class ProductPerTransactionRequestSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()

class TransactionRequestSerializer(serializers.Serializer):
    client = serializers.CharField(max_length=100)
    products = serializers.ListField(child=ProductPerTransactionRequestSerializer())
    payment_method = serializers.CharField(max_length=50)
    status = serializers.CharField(max_length=50)

    def create(self, validated_data):
        products_per_transaction = validated_data.pop('products')
        client = validated_data.pop('client')
        client = Client.objects.get(pk=client)
        products_per_transaction= [ProductPerTransaction(product=Product.objects.get(pk=product_per_transaction['product']),
                                                         quantity=product_per_transaction['quantity'],
                                                         total=0) for product_per_transaction in products_per_transaction]

        return Transaction(client=client, total=0, **validated_data), products_per_transaction

class TransactionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def map_to_entity(self, data) -> Transaction:
        data.pop('products')
        client = data.pop('client')
        client = Client(document=client)
        return Transaction(client=client, **data)