from rest_framework import serializers
from musicapp.models import User, SongCreated, FavoritesUser, Review, UserPrompt

# Serializador para el modelo User (Usuario)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'last_name', 'username', 'email', 'phone', 'pfp', 'is_active', 'is_staff']

# Serializador para el modelo SongCreated (Canción Creada)
class SongCreatedSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Anidamos el serializador de User para mostrar el usuario asociado

    class Meta:
        model = SongCreated
        fields = ['id', 'song_name', 'song_picture', 'audio_file', 'user', 'date']

# Serializador para el modelo FavoritesUser (Favoritos del Usuario)
class FavoritesUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Anidamos el serializador de User
    song = SongCreatedSerializer(read_only=True)  # Anidamos el serializador de SongCreated

    class Meta:
        model = FavoritesUser
        fields = ['id', 'user', 'song', 'added_on']

# Serializador para el modelo Review (Reseña)
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Anidamos el serializador de User
    song = SongCreatedSerializer(read_only=True)  # Anidamos el serializador de SongCreated

    class Meta:
        model = Review
        fields = ['id', 'user', 'song', 'date', 'review', 'punishment']

# Serializador para el modelo UserPrompt (Prompt del Usuario)
class UserPromptSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Anidamos el serializador de User

    class Meta:
        model = UserPrompt
        fields = ['id', 'user', 'prompt', 'date']
