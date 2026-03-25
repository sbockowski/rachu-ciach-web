from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from apps.budgets.models import Budget
from apps.budgets.services import budget_utilization_rate


class BudgetsListView(LoginRequiredMixin, ListView):
    template_name = 'dashboard.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budgets = self.get_queryset()
        context['budgets_with_utilization'] = []
        for budget in budgets:
            utilization = budget_utilization_rate(budget)
            context['budgets_with_utilization'].append({"budget": budget, "utilization": utilization})

        return context