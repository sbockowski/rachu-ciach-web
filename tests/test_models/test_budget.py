import pytest
from apps.budgets.models import Budget
from tests.factories import BudgetFactory

pytestmark = pytest.mark.django_db


def test_budget_created():
    budget = BudgetFactory()
    assert Budget.objects.get(id=budget.id)

def test_transaction_date():
    budget = BudgetFactory()
    assert budget.date_to > budget.date_from
