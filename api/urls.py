from django.urls import path
from .views import TrolleyView, TrolleyInfo, FrontLabelListCreateAPIView, BackLabelListCreateAPIView

urlpatterns = [
    path('trolleys/', TrolleyView.as_view(), name='trolley-list-create'),
    path('trolleys/<int:pk>/', TrolleyInfo.as_view(), name='trolley-detail'),
    path('trolleys/<int:trolley_id>/front-labels/', FrontLabelListCreateAPIView.as_view(), name='frontlabel-list-create'),
    path('trolleys/<int:trolley_id>/back-labels/', BackLabelListCreateAPIView.as_view(), name='backlabel-list-create'),
]