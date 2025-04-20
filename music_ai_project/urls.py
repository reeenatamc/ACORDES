# music_ai_project/urls.py

from django.contrib import admin
from django.urls import path, include
from musicapp.views import PromptFormView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('admin/', admin.site.urls),

  # Carga todas las rutas de tu API bajo /api/
  path('api/', include('apis.urls')),

  # Si quieres exponer tu formulario de prompts en la raíz
  path('', PromptFormView.as_view(), name='prompt-form'),
]

# Sirve media (y solo en DEBUG)
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
