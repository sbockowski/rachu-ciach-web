from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy

from apps.budgets.forms import BudgetForm
from apps.budgets.models import Budget

class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budget_create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BudgetDetailView(LoginRequiredMixin, DetailView):
    model = Budget
    template_name = 'budget_detail.html'