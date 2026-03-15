from django.contrib import admin
from .models import Category, Budget, BudgetPlan

admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(BudgetPlan)