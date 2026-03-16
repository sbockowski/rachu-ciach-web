from rest_framework import serializers
from apps.budgets.models import Category, Budget, BudgetPlan
from apps.savings.models import SavingsSnapshot
from apps.transactions.models import Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'type', 'is_system']
        read_only_fields = ['id', 'user', 'is_system']


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'user', 'name', 'type', 'date_from', 'date_to', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class BudgetPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetPlan
        fields = ['id', 'budget', 'category', 'planned_amount']
        read_only_fields = ['id', 'budget', 'category', 'planned_amount']


class SavingSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsSnapshot
        fields = ['id', 'user', 'budget', 'category', 'balance', 'note', 'snapshot_date']
        read_only_fields = ['id', 'user']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'budget', 'category', 'amount', 'type', 'date', 'description', 'source', 'created_at']
        read_only_fields = ['id', 'user', 'source', 'created_at']