from django.contrib import admin
from django.urls import path

from apps.budgets.views import BudgetListView, BudgetDetailView, CategoryListView, CategoryDetailView

urlpatterns = [
    path('api/budgets/', BudgetListView.as_view(), name='budget_list'),
    path('api/budgets/<pk>', BudgetDetailView.as_view(), name='budget_detail'),
    path('api/categories/', CategoryListView.as_view(), name='category_list'),
    path('api/categories/<pk>', CategoryDetailView.as_view(), name='budget_detail'),
]