from rest_framework import generics, permissions
from .models import Trolley, FrontLabel, BackLabel
from .serializers import TrolleySerializer, FrontLabelSerializer, BackLabelSerializer

# Create your views here.

class TrolleyView(generics.ListCreateAPIView):
    queryset = Trolley.objects.all()
    serializer_class = TrolleySerializer
    permission_classes = [permissions.IsAuthenticated]  # adjust permissions as needed

    def get_queryset(self):
        # You can customize filtering here if needed
        return super().get_queryset()


class TrolleyInfo(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trolley.objects.all()
    serializer_class = TrolleySerializer
    permission_classes = [permissions.IsAuthenticated]


class FrontLabelListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FrontLabelSerializer

    def get_queryset(self):
        trolley_id = self.kwargs['trolley_id']
        return FrontLabel.objects.filter(trolley_id=trolley_id)

    def perform_create(self, serializer):
        trolley_id = self.kwargs['trolley_id']
        # Optionally, add extra validation if trolley exists etc.
        serializer.save(trolley_id=trolley_id)


class BackLabelListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BackLabelSerializer

    def get_queryset(self):
        trolley_id = self.kwargs['trolley_id']
        return BackLabel.objects.filter(trolley_id=trolley_id)

    def perform_create(self, serializer):
        trolley_id = self.kwargs['trolley_id']
        serializer.save(trolley_id=trolley_id)

class FrontLabelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FrontLabel.objects.all()
    serializer_class = FrontLabelSerializer

class BackLabelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BackLabel.objects.all()
    serializer_class = BackLabelSerializer