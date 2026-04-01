from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from apps.budgets.models import Category
from apps.transactions.forms import TransactionForm
from apps.transactions.models import Transaction


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction_form.html'
    success_url = reverse_lazy('dashboard')

    def get_initial(self):
        initial = super().get_initial()
        budget_pk = self.request.GET.get('budget')
        if budget_pk:
            initial['budget'] = budget_pk
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transaction_form.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

def get_transaction_type(request):
    category_pk = request.GET.get('category')
    category = Category.objects.get(pk=category_pk)

    context = {
        'is_saving': category.type == 'saving',
        'category_type': category.type,
        'current_type': request.GET.get('current_type', '')
    }
    return render(request, "transaction_type_field.html", context=context)