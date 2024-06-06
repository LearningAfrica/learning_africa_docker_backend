from django.urls import path

from .views import RegisterViewSet, LoginViewSet, RefreshTokenViewSet, ChangePasswordViewSet

urlpatterns = [
    path('register/', RegisterViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', LoginViewSet.as_view({'post': 'create'}), name='login'),
    path('refresh_token/', RefreshTokenViewSet.as_view({'post': 'create'}), name='refresh_token'),
    path('change_password/', ChangePasswordViewSet.as_view({'post': 'update'}), name='change_password'),
]