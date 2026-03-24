from django.urls import path

from apps.savings.views.api import SavingsSnapshotListView, SavingsSnapshotDetailView

urlpatterns = [
    path('api/savings/', SavingsSnapshotListView.as_view(), name='savings_list'),
    path('api/savings/<pk>/', SavingsSnapshotDetailView.as_view(), name='savings_detail'),
]