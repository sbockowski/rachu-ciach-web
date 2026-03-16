from rest_framework import serializers
from apps.savings.models import SavingsSnapshot


class SavingSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsSnapshot
        fields = ['id', 'user', 'budget', 'category', 'balance', 'note', 'snapshot_date']
        read_only_fields = ['id', 'user']
