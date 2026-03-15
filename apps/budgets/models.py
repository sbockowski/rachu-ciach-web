import uuid
from django.conf import settings
from django.db import models


class Category(models.Model):
    class Type(models.TextChoices):
        EXPENSE = 'expense'
        INCOME = 'income'
        SAVING = 'saving'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, blank=True)
    type = models.CharField(max_length=10, choices=Type.choices)
    is_system = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.name} ({self.type})'

class Budget(models.Model):
    class Type(models.TextChoices):
        MONTHLY  = 'monthly', 'Monthly'
        YEARLY   = 'yearly', 'Yearly'
        WEEKLY   = 'weekly', 'Weekly'
        THEMATIC = 'thematic', 'Thematic'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=10, choices=Type.choices)
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.date_from} - {self.date_to})'

class BudgetPlan(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='plans')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    planned_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['budget', 'category']

    def __str__(self):
        return f'{self.budget} — {self.category}: {self.planned_amount}'