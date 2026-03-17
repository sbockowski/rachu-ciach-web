from django.contrib import admin
from django.urls import path

from apps.budgets.views import BudgetListView

urlpatterns = [
    path('api/budgets/', BudgetListView.as_view(), name='budget_list'),
]