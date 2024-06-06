from django.urls import path
from . import views

# router.register('super_admin', views.SuperAdminInvitationViewSet, basename='super_invite')
# router.register('admin', views.InvitationViewSet, basename='invitation')

urlpatterns = [
    path('super_admin/', views.SuperAdminInvitationViewSet.as_view({'post': 'create'}), name='super_admin_invite'),
    path('admin/', views.AdminInvitationViewSet.as_view({'post': 'create'}, name='admin_invite')),
]