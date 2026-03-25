from django.urls import path

from apps.budgets.views.ui import BudgetCreateView

urlpatterns = [
    path('budgets/create', BudgetCreateView.as_view(), name='budget_create'),
]