# apis/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apis.views import (
    UserViewSet,
    SongCreatedViewSet,
    FavoritesUserViewSet,
    ReviewViewSet,
    UserPromptViewSet,
    login,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'songs', SongCreatedViewSet, basename='song')
router.register(r'favorites', FavoritesUserViewSet, basename='favorite')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'prompts', UserPromptViewSet, basename='prompt')

urlpatterns = [
  # Todas las rutas registradas con router: /api/users/, /api/songs/, etc.
  path('', include(router.urls)),

  # Login “manual” (si no usas un ViewSet para esto)
  path('login/', login, name='login'),

  # JWT endpoints
  path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
