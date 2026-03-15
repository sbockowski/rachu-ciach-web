import uuid
from django.db import models
from django.conf import settings
from apps.budgets.models import Budget, Category

class SavingsSnapshot(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    budget        = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='snapshots')
    category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    balance       = models.DecimalField(max_digits=10, decimal_places=2)
    note          = models.CharField(max_length=255, blank=True)
    snapshot_date = models.DateField()

    class Meta:
        ordering = ['-snapshot_date']
        indexes  = [
            models.Index(fields=['user', 'category']),
        ]

    def __str__(self):
        return f'{self.category.name}: {self.balance}zł ({self.snapshot_date})'