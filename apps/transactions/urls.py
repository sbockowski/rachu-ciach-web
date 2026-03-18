from django.urls import path

from apps.transactions.views import TransactionListView, TransactionDetailView

urlpatterns = [
    path('api/transactions/', TransactionListView.as_view(), name='transactions_list'),
    path('api/transactions/<pk>', TransactionDetailView.as_view(), name='transactions_detail'),
]