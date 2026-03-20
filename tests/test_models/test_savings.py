from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError
from apps.savings.models import SavingsSnapshot
from tests.factories import SavingsSnapshotFactory

pytestmark = pytest.mark.django_db


def test_savings_snapshot_created():
    saving = SavingsSnapshotFactory()
    assert SavingsSnapshot.objects.get(id=saving.id)

@pytest.mark.parametrize("amount", [0, -2, -100])
def test_invalid_balance(amount):
    saving = SavingsSnapshotFactory(balance=amount)
    with pytest.raises(ValidationError):
        saving.full_clean()

@pytest.mark.parametrize("test_date", [date.today() + timedelta(days=2), date.today() + timedelta(days=100)])
def test_incorrect_snapshot_date(test_date):
    saving = SavingsSnapshotFactory(snapshot_date=test_date)
    with pytest.raises(ValidationError):
        saving.full_clean()

def test_savings_snapshot_user():
    saving = SavingsSnapshotFactory()
    assert saving.category.user == saving.user