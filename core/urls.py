from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from visitas.views import VisitaViewSet

router = DefaultRouter()
router.register('visitas', VisitaViewSet, basename='visita')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('visitas.urls')),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
