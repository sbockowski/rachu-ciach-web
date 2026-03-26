from django.urls import path

from apps.transactions.views.ui import TransactionCreateView

urlpatterns = [
    path('transactions/create', TransactionCreateView.as_view(), name='transaction_create'),
    # path('budgets/<pk>/update/', BudgetUpdateView.as_view(), name='budget_update'),
    # path('budgets/<pk>/delete/', BudgetDeleteView.as_view(), name='budget_delete'),
    # path('budgets/<pk>/', BudgetDetailView.as_view(), name='budget_detail'),
]