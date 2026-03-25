from django.urls import path

from apps.budgets.views.ui import BudgetCreateView, BudgetDetailView

urlpatterns = [
    path('budgets/create', BudgetCreateView.as_view(), name='budget_create'),
    path('budgets/<pk>/', BudgetDetailView.as_view(), name='budget_detail'),
]