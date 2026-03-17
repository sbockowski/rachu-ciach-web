from datetime import date

import pytest
from django.core.exceptions import ValidationError

from apps.budgets.models import Budget
from tests.factories import BudgetFactory

pytestmark = pytest.mark.django_db


def test_budget_created():
    budget = BudgetFactory()
    assert Budget.objects.get(id=budget.id)

def test_budget_date():
    budget = BudgetFactory()
    assert budget.date_to > budget.date_from

def test_budget_incorrect_dates():
    budget = BudgetFactory(date_from=date(2025, 3, 15), date_to=date(2025, 3, 1))
    with pytest.raises(ValidationError):
        budget.clean()

def test_budget_equal_dates():
    budget = BudgetFactory(date_from=date(2025, 3, 1), date_to=date(2025, 3, 1))
    with pytest.raises(ValidationError):
        budget.clean()
