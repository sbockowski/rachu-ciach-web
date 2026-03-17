from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from apps.transactions.models import Transaction
from tests.factories import TransactionFactory

pytestmark = pytest.mark.django_db


def test_transaction_created():
    transaction = TransactionFactory()
    assert Transaction.objects.get(id=transaction.id)

@pytest.mark.parametrize("amount", [0, -2, -100])
def test_transaction_amount(amount):
    transaction = TransactionFactory(amount=amount)
    with pytest.raises(ValidationError):
        transaction.full_clean()

def test_transaction_date_out_of_budget():
    transaction = TransactionFactory()
    transaction.date = transaction.budget.date_to + timedelta(days=1)
    with pytest.raises(ValidationError):
        transaction.full_clean()

def test_transaction_user():
    transaction = TransactionFactory()
    assert transaction.budget.user == transaction.user
    assert transaction.category.user == transaction.user
