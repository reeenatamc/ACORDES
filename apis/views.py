from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.decorators import api_view

from musicapp.models import User, SongCreated, FavoritesUser, Review, UserPrompt
from apis.serializers import UserSerializer, SongCreatedSerializer, FavoritesUserSerializer, ReviewSerializer, UserPromptSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

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

# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#
#     # Autenticación del usuario
#     user = authenticate(username=username, password=password)
#
#     if user is not None:
#         # Crear o recuperar el token de autenticación
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key}, status=status.HTTP_200_OK)
#     else:
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Buscar el usuario por su email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    # Autenticación del usuario con el email y la contraseña
    user = authenticate(username=user.username, password=password)

    if user is not None:
        # Crear o recuperar el token de autenticación
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
