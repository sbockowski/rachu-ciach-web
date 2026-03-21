from django.db.models import Q
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Budget, Category, BudgetPlan
from .serializers import BudgetSerializer, CategorySerializer, BudgetPlanSerializer


class BudgetListView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        budgets = Budget.objects.filter(user=request.user)
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BudgetDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return Budget.objects.get(id=pk, user=request.user)
        except Budget.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        budget = self.get_object(request, pk)
        serializer = BudgetSerializer(budget)
        return Response(serializer.data)

    def put(self, request, pk):
        budget = self.get_object(request, pk)
        serializer = BudgetSerializer(budget, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        budget = self.get_object(request, pk)
        budget.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(Q(user=request.user) | Q(is_system=True))
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request, pk):
        category = Category.objects.filter(id=pk).first()
        if category is None:
            raise Http404
        if category.user != request.user and not category.is_system:
            raise Http404
        return category

    def get(self, request, pk):
        category = self.get_object(request, pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(request, pk)
        if category.is_system:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = CategorySerializer(category, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(request, pk)
        if category.is_system:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class BudgetPlanListView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        budget_plans = BudgetPlan.objects.filter(budget__user=request.user)
        serializer = BudgetPlanSerializer(budget_plans, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BudgetPlanSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BudgetPlanDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return BudgetPlan.objects.get(id=pk, budget__user=request.user)
        except BudgetPlan.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        budget_plan = self.get_object(request, pk)
        serializer = BudgetPlanSerializer(budget_plan)
        return Response(serializer.data)

    def put(self, request, pk):
        budget_plan = self.get_object(request, pk)
        serializer = BudgetPlanSerializer(budget_plan, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        budget_plan = self.get_object(request, pk)
        budget_plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
