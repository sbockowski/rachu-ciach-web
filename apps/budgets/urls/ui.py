from django.urls import path

from apps.budgets.views.ui import BudgetCreateView, BudgetDetailView, BudgetUpdateView, BudgetDeleteView

urlpatterns = [
    path('budgets/create', BudgetCreateView.as_view(), name='budget_create'),
    path('budgets/<pk>/update/', BudgetUpdateView.as_view(), name='budget_update'),
    path('budgets/<pk>/delete/', BudgetDeleteView.as_view(), name='budget_delete'),
    path('budgets/<pk>/', BudgetDetailView.as_view(), name='budget_detail'),
]