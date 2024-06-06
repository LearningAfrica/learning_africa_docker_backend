from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
import debug_toolbar

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='Learning Africa API',
        default_version='v1',
        description='API for Learning Africa Platform',
        contact=openapi.Contact(email='brianodhiambo530@gmail.com'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

admin.site.site_header = 'Learning Africa Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('users/', include('system_users.urls')),
    path('api/', include('courses.urls')),
    path('invite/', include('invitation_app.urls')),
    path('media/', serve, {'document_root': settings.MEDIA_ROOT}),
    path('__debug__/', include(debug_toolbar.urls)),
    path('redoc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)