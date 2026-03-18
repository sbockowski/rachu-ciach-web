from django.contrib import admin
from django.urls import path

from apps.budgets.views import BudgetListView, BudgetDetailView

urlpatterns = [
    path('api/budgets/', BudgetListView.as_view(), name='budget_list'),
    path('api/budgets/<pk>', BudgetDetailView.as_view(), name='budget_detail'),
]