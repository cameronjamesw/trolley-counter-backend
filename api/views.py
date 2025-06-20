from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Trolley, FrontLabel, BackLabel
from .serializers import (
    TrolleySerializer,
    FrontLabelSerializer,
    BackLabelSerializer,
)

# Create your views here.


class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })


class TrolleyView(generics.ListCreateAPIView):
    queryset = Trolley.objects.all()
    serializer_class = TrolleySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # You can customize filtering here if needed
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TrolleyInfo(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trolley.objects.all()
    serializer_class = TrolleySerializer
    permission_classes = [permissions.IsAuthenticated]


class FrontLabelListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FrontLabelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['trolley']
    queryset = FrontLabel.objects.all()

    def perform_create(self, serializer):
        trolley_id = self.kwargs['trolley_id']
        # Optionally, add extra validation if trolley exists etc.
        serializer.save(trolley_id=trolley_id)
        serializer.save(creator=self.request.user)


class BackLabelListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BackLabelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['trolley']
    queryset = BackLabel.objects.all()

    def perform_create(self, serializer):
        trolley_id = self.kwargs['trolley_id']
        serializer.save(trolley_id=trolley_id)
        serializer.save(creator=self.request.user)


class FrontLabelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FrontLabel.objects.all()
    serializer_class = FrontLabelSerializer


class BackLabelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BackLabel.objects.all()
    serializer_class = BackLabelSerializer
