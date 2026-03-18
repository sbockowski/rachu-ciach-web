from rest_framework import serializers
from apps.budgets.models import Category, Budget, BudgetPlan


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'type', 'is_system']
        read_only_fields = ['id', 'user', 'is_system']

    def validate(self, data):
        user = self.context['request'].user
        name = data.get('name')
        type_ = data.get('type') or self.instance.type
        if name and type_ and Category.objects.filter(user=user, name=name, type=type_).exists():
            raise serializers.ValidationError("Category with this name and type already exists.")
        return data

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'user', 'name', 'date_from', 'date_to', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        if data['date_to'] <= data['date_from']:
            raise serializers.ValidationError("Field 'date_to' cannot contain date before or equal to field 'date_from'")
        return data

class BudgetPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetPlan
        fields = ['id', 'budget', 'category', 'planned_amount']
        read_only_fields = ['id', 'budget', 'category', 'planned_amount']