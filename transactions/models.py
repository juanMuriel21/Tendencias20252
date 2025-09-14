import uuid

from django.db import models

from clients.models import Client
from products.models import Product


# Create your models here.

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="ProductPerTransaction")
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def to_dict(self):
        return {
            "id": self.id,
            "client": self.client.document,
            'products': [product.to_dict() for product in ProductPerTransaction.objects.filter(transaction_id=self.id).all()],
            "payment_method": self.payment_method,
            "status": self.status,
            "total": self.total,
        }

class ProductPerTransaction(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def to_dict(self):
        return {
            "product": self.product.name,
            "quantity": self.quantity,
            "total": self.total,
        }