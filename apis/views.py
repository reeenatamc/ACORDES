from rest_framework import viewsets
from musicapp.models import User, SongCreated, FavoritesUser, Review, UserPrompt
from apis.serializers import UserSerializer, SongCreatedSerializer, FavoritesUserSerializer, ReviewSerializer, UserPromptSerializer

# ViewSet para el modelo User (Usuario)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ViewSet para el modelo SongCreated (Canción Creada)
class SongCreatedViewSet(viewsets.ModelViewSet):
    queryset = SongCreated.objects.all()
    serializer_class = SongCreatedSerializer

# ViewSet para el modelo FavoritesUser (Favoritos del Usuario)
class FavoritesUserViewSet(viewsets.ModelViewSet):
    queryset = FavoritesUser.objects.all()
    serializer_class = FavoritesUserSerializer

# ViewSet para el modelo Review (Reseña)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# ViewSet para el modelo UserPrompt (Prompt del Usuario)
class UserPromptViewSet(viewsets.ModelViewSet):
    queryset = UserPrompt.objects.all()
    serializer_class = UserPromptSerializer
