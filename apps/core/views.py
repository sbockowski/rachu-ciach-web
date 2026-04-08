from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.budgets.models import Budget
from apps.budgets.services import budget_utilization_rate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from ..transactions.models import Transaction


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(
                request, f"Your account has been created! You are now able to log in."
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['budgets'] = Budget.objects.filter(user=self.request.user)
        context['transactions'] = Transaction.objects.filter(user=self.request.user)

        context['budgets_with_utilization'] = []
        for budget in context['budgets']:
            utilization = budget_utilization_rate(budget)
            context['budgets_with_utilization'].append({"budget": budget, "utilization": utilization})

        return context