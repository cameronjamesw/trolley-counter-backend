from django.urls import path, include
from .views import (
                    UserDetailView,
                    TrolleyView,
                    TrolleyInfo,
                    FrontLabelListCreateAPIView,
                    BackLabelListCreateAPIView,
                    FrontLabelDetailView,
                    BackLabelDetailView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('back-labels/', BackLabelListCreateAPIView.as_view(),
         name='back-label'),
    path('back-labels/<int:pk>/',
         BackLabelDetailView.as_view(), name='back-label-detail'),
    path('front-labels/', FrontLabelListCreateAPIView.as_view(),
         name="front-label"),
    path('front-labels/<int:pk>/',
         FrontLabelDetailView.as_view(), name='front-label-detail'),
    path('pinned/', include('pinned.urls')),
    path('api/user/',
         UserDetailView.as_view(), name='user-detail'),
    path('trolleys/',
         TrolleyView.as_view(), name='trolley-list-create'),
    path('trolleys/<int:pk>/',
         TrolleyInfo.as_view(), name='trolley-detail'),
    path('trolleys/<int:trolley_id>/front-labels/',
         FrontLabelListCreateAPIView.as_view(), name='frontlabel-list-create'),
    path('trolleys/<int:trolley_id>/back-labels/',
         BackLabelListCreateAPIView.as_view(), name='backlabel-list-create'),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/',
         TokenVerifyView.as_view(), name='token_verify'),
]
