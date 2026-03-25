from django import forms
from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'date_from', 'date_to']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'date_from': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'date_to': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
        }