from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import upload_csv


schema_view = get_schema_view(
    openapi.Info(
        title="O2Citi Serve Api",
        default_version='v1',
        description="API documentation for O2Citi Serve Plaform",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('menu.urls')),  # Include menu item URLs
    path('api/', include('orders.urls')),  # Include order URLs
    path('api/', include('authentication.urls')),  # Include user URLs
    path('api/', include('tables.urls')),  # Include user URLs
    path('api/', include('customers.urls')),  # Include user URLs

    # Swagger documentation URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload-csv/', upload_csv, name='upload_csv'),
]
