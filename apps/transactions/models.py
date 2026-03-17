import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from apps.budgets.models import Budget, Category


class Transaction(models.Model):
    class Type(models.TextChoices):
        EXPENSE = 'expense'
        INCOME = 'income'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    type = models.CharField(max_length=10, choices=Type.choices)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=20, default='web')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'budget']),
            models.Index(fields=['user', 'date']),
        ]

    def clean(self):
        if not (self.budget.date_from <= self.date <= self.budget.date_to):
            raise ValidationError("Transaction date must be within the budget period.")

    def __str__(self):
        return f'{self.type} {self.amount}zł — {self.category}'
