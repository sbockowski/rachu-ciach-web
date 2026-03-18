from rest_framework import serializers

from apps.budgets.models import Category
from apps.transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'budget', 'category', 'amount', 'type', 'date', 'description', 'source', 'created_at']
        read_only_fields = ['id', 'user', 'source', 'created_at']

    def validate(self, data):
        budget = data.get('budget') or self.instance.budget
        category = data.get('category') or self.instance.category
        date_ = data.get('date') or self.instance.date
        type_ = data.get('type') or self.instance.type

        if budget and budget.user != self.context['request'].user:
            raise serializers.ValidationError("You can't assign a budget that isn't yours.")

        if category and category.user != self.context['request'].user:
            raise serializers.ValidationError("You can't assign a category that isn't yours.")

        if not (budget.date_from <= date_ <= budget.date_to):
            raise serializers.ValidationError("Transaction date must be within the budget period.")

        if type_ in (Transaction.Type.SAVING_DEPOSIT, Transaction.Type.SAVING_WITHDRAWAL):
            if category.type != Category.Type.SAVING:
                raise serializers.ValidationError("Transaction type must be compatible with category type.")
        elif type_ != category.type:
            raise serializers.ValidationError("Transaction type must be compatible with category type.")

        return data

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value