from decimal import Decimal

from django.db.models.aggregates import Sum


def budget_utilization_rate(budget):
    planned_amount = budget.plans.filter(category__type='expense').aggregate(Sum('planned_amount'))['planned_amount__sum'] or Decimal('0')
    spent_amount = budget.transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or Decimal('0')

    has_plan = planned_amount > 0
    has_transactions = spent_amount > 0
    utilization_rate = 0

    if planned_amount > 0 and spent_amount > 0:
        utilization_rate = round(spent_amount/planned_amount * 100)

    return {
        "has_plan": has_plan,
        "has_transactions": has_transactions,
        "spent_amount":spent_amount,
        "planned_amount": planned_amount,
        "utilization_rate": utilization_rate
    }
