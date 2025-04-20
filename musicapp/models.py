from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group

# Modelo de Usuario
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    pfp = models.ImageField(upload_to='users', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
# Modelo de Canción Creada
class SongCreated(models.Model):
    song_name = models.TextField(null=True, blank=True)
    song_picture = models.ImageField(upload_to='picture_songs', null=True, blank=True)
    audio_file = models.FileField(upload_to='songs', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.song_name

# Modelo de Favoritos
class FavoritesUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey(SongCreated, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')

    def __str__(self):
        return f"{self.user.name} - {self.song.song_name}"

# Modelo de Reseña
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey(SongCreated, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    review = models.TextField()
    punishment = models.IntegerField(default=0)

    def __str__(self):
        return self.review

class UserPrompt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prompt = models.TextField()  # Almacenamos el prompt como texto
    date = models.DateTimeField(auto_now_add=True)  # Fecha en que se registró el prompt

    def __str__(self):
        return f"Prompt by {self.user.username} on {self.date}"