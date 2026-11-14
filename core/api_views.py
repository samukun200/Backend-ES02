from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class PublicTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)


class PublicTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)
