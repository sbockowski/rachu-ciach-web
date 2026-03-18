from datetime import date

from rest_framework import serializers

from apps.budgets.models import Category
from apps.savings.models import SavingsSnapshot


class SavingSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsSnapshot
        fields = ['id', 'user', 'category', 'balance', 'note', 'snapshot_date']
        read_only_fields = ['id', 'user']

    def validate(self, data):
        category = data.get('category') or self.instance.category
        snapshot_date = data.get('snapshot_date') or self.instance.snapshot_date

        if category and category.user != self.context['request'].user:
            raise serializers.ValidationError("You can't assign a category that isn't yours.")

        if category and category.type != Category.Type.SAVING:
            raise serializers.ValidationError("SavingsSnapshot requires a category of type 'saving'.")

        if snapshot_date > date.today():
            raise serializers.ValidationError("Snapshot date cannot be in the future.")

        return data


    def validate_balance(self, value):
        if value <= 0:
            raise serializers.ValidationError("Balance must be greater than 0.")
        return value