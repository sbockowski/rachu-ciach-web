from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import SavingsSnapshot
from .serializers import SavingSnapshotSerializer


class SavingsSnapshotListView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        savings = SavingsSnapshot.objects.filter(user=request.user)
        serializer = SavingSnapshotSerializer(savings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SavingSnapshotSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavingsSnapshotDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return SavingsSnapshot.objects.get(id=pk, user=request.user)
        except SavingsSnapshot.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        savings_snapshot = self.get_object(request, pk)
        serializer = SavingSnapshotSerializer(savings_snapshot)
        return Response(serializer.data)

    def put(self, request, pk):
        savings_snapshot = self.get_object(request, pk)
        serializer = SavingSnapshotSerializer(savings_snapshot, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        savings_snapshot = self.get_object(request, pk)
        savings_snapshot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)