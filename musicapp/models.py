from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group

# Modelo de Usuario
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    pfp = models.ImageField(upload_to='users', null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Si el usuario es admin
    is_superuser = models.BooleanField(default=False)  # Para el superusuario

    objects = UserManager()  # El UserManager personalizado

    USERNAME_FIELD = 'email'  # Usamos el email para iniciar sesión
    REQUIRED_FIELDS = ['username']  # Otros campos obligatorios

    def __str__(self):
        return self.username

    # Aquí añadimos related_name para evitar la ambigüedad
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True
    )

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True
    )


# Modelo de Canción Creada
class SongCreated(models.Model):
    song_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.song_name

# Modelo de Favoritos
class FavoritesUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(SongCreated, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')  # Asegura que un usuario no pueda marcar la misma canción más de una vez

    def __str__(self):
        return f"{self.user.name} - {self.song.song_name}"

# Modelo de Reseña
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(SongCreated, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    review = models.TextField()
    punishment = models.IntegerField(default=0)

    def __str__(self):
        return self.review

class UserPrompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()  # Almacenamos el prompt como texto
    date = models.DateTimeField(auto_now_add=True)  # Fecha en que se registró el prompt

    def __str__(self):
        return f"Prompt by {self.user.username} on {self.date}"