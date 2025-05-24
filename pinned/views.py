from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Pinned
from .serializers import PinnedSerializer

# Create your views here.

class PinnedList(generics.ListCreateAPIView):
    permission_classes = permissions.IsAuthenticatedOrReadOnly
    queryset = Pinned.objects.all()
    serializer_class = PinnedSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class PinnedDetail(generics.RetrieveDestroyAPIView):
    permission_classes = permissions.IsAuthenticated
    serializer_class = PinnedSerializer
    queryset = Pinned.objects.all()