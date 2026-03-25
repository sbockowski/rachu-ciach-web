from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from .forms import UserRegisterForm
from apps.budgets.models import Budget
from ..budgets.services import budget_utilization_rate


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