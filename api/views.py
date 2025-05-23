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
