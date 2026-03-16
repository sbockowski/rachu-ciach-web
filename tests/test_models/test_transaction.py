import pytest

from apps.transactions.models import Transaction
from tests.factories import TransactionFactory


@pytest.mark.django_db
def test_transaction_created():
    transaction = TransactionFactory()
    assert Transaction.objects.get(id=transaction.id)


@pytest.mark.django_db
def test_transaction_amount():
    transaction = TransactionFactory()
    transaction_amount = transaction.amount

    assert transaction_amount > 0


@pytest.mark.django_db
def test_transaction_date():
    transaction = TransactionFactory()
    transaction_date = transaction.date

    assert transaction.budget.date_from <= transaction_date <= transaction.budget.date_to


@pytest.mark.django_db
def test_transaction_user():
    transaction = TransactionFactory()
    transaction_user = transaction.user

    assert transaction.budget.user == transaction_user
