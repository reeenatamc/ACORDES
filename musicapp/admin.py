from django.contrib import admin
from .models import User, SongCreated, FavoritesUser, Review, UserPrompt
from unfold.admin import ModelAdmin
# Administrador para el modelo User
class UserAdmin(ModelAdmin):
    list_display = ('username', 'name', 'last_name', 'email', 'phone')
    search_fields = ('username', 'name', 'email')
    ordering = ('name',)
    list_filter = ('name',)

admin.site.register(User, UserAdmin)

# Administrador para el modelo SongCreated
class SongCreatedAdmin(ModelAdmin):
    list_display = ('song_name', 'user', 'date')
    search_fields = ('song_name',)
    ordering = ('date',)
    list_filter = ('user', 'date')

admin.site.register(SongCreated, SongCreatedAdmin)

# Administrador para el modelo FavoritesUser
class FavoritesUserAdmin(ModelAdmin):
    list_display = ('user', 'song', 'added_on')
    search_fields = ('user__username', 'song__song_name')
    ordering = ('added_on',)
    list_filter = ('user',)

admin.site.register(FavoritesUser, FavoritesUserAdmin)

# Administrador para el modelo Review
class ReviewAdmin(ModelAdmin):
    list_display = ('user', 'song', 'date', 'punishment')  # Campos a mostrar en la lista
    search_fields = ('user__username', 'song__song_name', 'review')  # Búsqueda por usuario, canción y reseña
    ordering = ('date',)  # Orden por fecha
    list_filter = ('user', 'song')  # Filtro por usuario y canción

admin.site.register(Review, ReviewAdmin)

# Administrador para el modelo UserPrompt
class UserPromptAdmin(ModelAdmin):
    list_display = ('user', 'date', 'prompt')
    search_fields = ('user__username', 'prompt')
    ordering = ('date',)
    list_filter = ('user',)

admin.site.register(UserPrompt, UserPromptAdmin)
