from django import forms
from django.db.models import Q

from .models import Transaction
from apps.budgets.models import Budget, Category


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(user=user)
        self.fields['category'].queryset = Category.objects.filter(Q(user=user) | Q(is_system = True))

    class Meta:
        model = Transaction
        fields = ['budget', 'category', 'amount', 'type', 'date', 'description']
        widgets = {
            'budget': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'category': forms.Select(attrs={'class': 'select select-bordered w-full',
                                            'hx-get': '/transactions/category-type/',
                                            'hx-target': '#transaction-type-container',
                                            'hx-trigger': 'change'
        }),
            'amount': forms.NumberInput(attrs={'class': 'grow', 'placeholder': '0.00 PLN'}),
            'date': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'input input-bordered w-full',}),
        }