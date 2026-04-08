from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.context_processors import request
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

from apps.budgets.forms import BudgetForm
from apps.budgets.models import Budget


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budget_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'budget_form.html'

    def get_success_url(self):
        return reverse_lazy('budget_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

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