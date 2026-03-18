from django.urls import path

from apps.budgets.views import (
    BudgetListView, BudgetDetailView,
    CategoryListView, CategoryDetailView, \
    BudgetPlanDetailView, BudgetPlanListView
)

urlpatterns = [
    path('api/budgets/', BudgetListView.as_view(), name='budget_list'),
    path('api/budgets/<pk>', BudgetDetailView.as_view(), name='budget_detail'),
    path('api/categories/', CategoryListView.as_view(), name='category_list'),
    path('api/categories/<pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('api/budget_plans/', BudgetPlanListView.as_view(), name='budget_plan_list'),
    path('api/budget_plans/<pk>', BudgetPlanDetailView.as_view(), name='budget_plan_detail'),
]