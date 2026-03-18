from rest_framework import serializers
from apps.budgets.models import Category, Budget, BudgetPlan


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'type', 'is_system']
        read_only_fields = ['id', 'user', 'is_system']

    def validate(self, data):
        user = self.context['request'].user
        name = data.get('name') or self.instance.name
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
        read_only_fields = ['id']

    def validate(self, data):
        budget = data.get('budget') or self.instance.budget
        category = data.get('category') or self.instance.category

        if budget and budget.user != self.context['request'].user:
            raise serializers.ValidationError("You can't assign a budget that isn't yours.")

        if category and category.user != self.context['request'].user:
            raise serializers.ValidationError("You can't assign a category that isn't yours.")

        if budget and category and BudgetPlan.objects.filter(budget=budget, category=category).exists():
            raise serializers.ValidationError("BudgetPlan in this budget and with this category already exists.")

        return data
