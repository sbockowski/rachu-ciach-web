import pytest
from apps.transactions.models import Transaction
from tests.factories import TransactionFactory

pytestmark = pytest.mark.django_db


def test_transaction_created():
    transaction = TransactionFactory()
    assert Transaction.objects.get(id=transaction.id)


def test_transaction_amount():
    transaction = TransactionFactory()
    assert transaction.amount > 0


def test_transaction_date():
    transaction = TransactionFactory()
    assert transaction.budget.date_from <= transaction.date <= transaction.budget.date_to


def test_transaction_user():
    transaction = TransactionFactory()
    assert transaction.budget.user == transaction.user
