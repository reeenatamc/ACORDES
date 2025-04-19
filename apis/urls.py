from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apis.views import UserViewSet, SongCreatedViewSet, FavoritesUserViewSet, ReviewViewSet, UserPromptViewSet

# Crear un router y registrar nuestros viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'songs', SongCreatedViewSet)
router.register(r'favorites', FavoritesUserViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'prompts', UserPromptViewSet)

# Definir las URLs
urlpatterns = [
    path('api/', include(router.urls)),  # Aquí se incluirán todas las rutas de los viewsets
]
