from django.urls import path
from .views import TrolleyView, TrolleyInfo

urlpatterns = [
    path('trolleys/', TrolleyView.as_view(), name='trolley-list-create'),
    path('trolleys/<int:pk>/', TrolleyInfo.as_view(), name='trolley-detail'),
]