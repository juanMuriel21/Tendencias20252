from decimal import Decimal

from django.test import TestCase, Client
from rest_framework import status

from products.models import Product
from products.services import ProductService


# Create your tests here.

class ProductTestCase(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.product_service = ProductService()
        self.product = Product(id=1)

    def setUp(self):
        self.client = Client()


    def test_create_product_successfully(self):
        product_request: dict[str, object] = {
            "name": "Test Product",
            "category":"Test Category",
            "subcategory": "Test Sub Category",
            "price": '15000.00',
            "quantity": 5,
        }
        response = self.client.post("/api/products/", product_request, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), {
            "id": 1,
            **product_request
        })
        
    def test_get_product_by_id_successfully(self):
        Product.objects.create(
            name="Another Product",
            category="Another Category",
            subcategory="Another Subcategory",
            price=25000.00,
            quantity=15
        )

        product = self.product_service.get_product_by_id(self.product.id)

        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, 'Another Product')
        self.assertEqual(product.category, 'Another Category')
        self.assertEqual(product.subcategory, 'Another Subcategory')
        self.assertEqual(product.price, Decimal('25000.00'))
        self.assertEqual(product.quantity, 15)

    def test_get_all_products_successfully(self):
        Product.objects.create(
            name="Another Product",
            category="Another Category",
            subcategory="Another Subcategory",
            price=25000.00,
            quantity=15
        )

        Product.objects.create(
            name="Another Product 2",
            category="Another Category 2",
            subcategory="Another Subcategory 2",
            price=8000.00,
            quantity=2
        )

        products = self.product_service.get_all_products()
        self.assertEqual(len(products), 2)

    def test_update_product_successfully(self):
        Product.objects.create(
            name="Another Product",
            category="Another Category",
            subcategory="Another Subcategory",
            price=25000.00,
            quantity=15
        )

        updated_product = Product(
            id='1',
            name="Updated Product",
            category="Updated Category",
            subcategory="Updated Subcategory",
            price=20000.00,
            quantity=10
        )

        updated_product_instance = self.product_service.update_product(updated_product)

        self.assertEqual(updated_product_instance.name, "Updated Product")
        self.assertEqual(updated_product_instance.category, "Updated Category")

    def test_delete_product_successfully(self):
        Product.objects.create(
            name="Another Product",
            category="Another Category",
            subcategory="Another Subcategory",
            price=25000.00,
            quantity=15
        )

        product_id = self.product.id
        self.product_service.delete_product(product_id)

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=product_id)
