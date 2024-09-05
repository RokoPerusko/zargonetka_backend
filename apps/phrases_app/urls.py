from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ZargonetkaProjekt.urls import schema_view
from .views import PhrasesViewSet

router = DefaultRouter()
router.register(r'', PhrasesViewSet, basename='phrases')  # Register the new viewset

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
