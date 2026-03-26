from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.context_processors import request
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

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['budget_plans'] = self.object.plans.all()
        context['transactions'] = self.object.transactions.all()

        return context