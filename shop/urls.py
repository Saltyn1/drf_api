from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter

from main.views import ProductViewSet, ReviewViewSet, OrderViewSet

router = SimpleRouter()
router.register('products', ProductViewSet)
router.register('reviews', ReviewViewSet)
router.register('orders', OrderViewSet)


# документация
schema_view = get_schema_view(
    openapi.Info(
        title='My API',
        default_version='v1',
        description='My ecommerce API'
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),
    path('api/v1/docs/', schema_view.with_ui('swagger')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)