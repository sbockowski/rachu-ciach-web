import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from apps.budgets.models import BudgetPlan
from tests.factories import BudgetPlanFactory, CategoryFactory, BudgetFactory

pytestmark = pytest.mark.django_db


def test_budget_plan_created():
    budget_plan = BudgetPlanFactory()
    assert BudgetPlan.objects.get(id=budget_plan.id)

@pytest.mark.parametrize("amount", [0, -2, -100])
def test_invalid_planned_amount(amount):
    budget_plan = BudgetPlanFactory(planned_amount=amount)
    with pytest.raises(ValidationError):
        budget_plan.full_clean()

def test_budget_plan_unique():
    test_budget = BudgetFactory()
    test_category = CategoryFactory()
    BudgetPlanFactory(budget=test_budget, category=test_category)
    with pytest.raises(IntegrityError):
        BudgetPlanFactory(budget=test_budget, category=test_category)