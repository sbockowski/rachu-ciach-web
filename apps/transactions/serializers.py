from rest_framework import serializers
from apps.savings.models import SavingsSnapshot
from apps.transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'budget', 'category', 'amount', 'type', 'date', 'description', 'source', 'created_at']
        read_only_fields = ['id', 'user', 'source', 'created_at']