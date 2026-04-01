from django.urls import path

from apps.transactions.views.ui import TransactionCreateView, get_transaction_type, TransactionUpdateView, TransactionDeleteView

urlpatterns = [
    path('transactions/create/', TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/category-type/', get_transaction_type, name='transaction_category_type'),
    path('transactions/<pk>/update/', TransactionUpdateView.as_view(), name='transaction_update'),
    path('transactions/<pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
]