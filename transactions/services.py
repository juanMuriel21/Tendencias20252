from uuid import UUID

from django.db.models import QuerySet

from transactions.models import Transaction, ProductPerTransaction
from transactions.serializers import TransactionDataSerializer


class TransactionService:
    def create_transaction(self, transaction: Transaction, products_per_transaction: list[ProductPerTransaction]) -> Transaction:
        transaction.status = 'PAGADO'
        for product_per_transaction in products_per_transaction:
            product_per_transaction.transaction = transaction
            product_per_transaction.total = product_per_transaction.product.price * product_per_transaction.quantity
            transaction.total += product_per_transaction.total

        data_serializer = TransactionDataSerializer(data=transaction.to_dict())
        if data_serializer.is_valid(raise_exception=True):
            data_serializer.save()
            data_saved = data_serializer.data
            for product_per_transaction in products_per_transaction:
                product_per_transaction.save()
            return data_serializer.map_to_entity(data_saved)

        raise Exception("Ocurrio un error al efectuar la transaccion")

    def get_transactions_by_id(self, transaction_id: UUID) -> Transaction:
        return Transaction.objects.get(id=transaction_id)

    def get_all_transactions(self) -> QuerySet:
        return Transaction.objects.all()

    def get_transaction_to_update(self, old_transaction: Transaction, transaction_to_update: Transaction) -> Transaction:
        old_transaction.status = transaction_to_update.status
        return old_transaction

    def update_transaction(self, transaction: Transaction) -> Transaction | None:
        old_transaction: Transaction = self.get_transactions_by_id(transaction.id)
        updated_transaction = self.get_transaction_to_update(old_transaction, transaction)
        Transaction.objects.bulk_update(objs=[updated_transaction], fields=['status'])
        return updated_transaction

    def delete_transaction(self, transaction_id: UUID) -> None:
        transaction = self.get_transactions_by_id(transaction_id)
        transaction.delete()