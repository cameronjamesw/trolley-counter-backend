from django.urls import path
from .views import PinnedList, PinnedDetail

urlpatterns = [
    path("", PinnedList.as_view(), name="pinned-trolleys"),
    path("<int:pk>/", PinnedDetail.as_view(), name="pinned-trolley-detail"),
]