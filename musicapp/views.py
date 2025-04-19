import os

from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from musicapp.forms import PromptForm
from musicapp.models import UserPrompt, SongCreated
from musicapp.services import MusicService
from musicapp.utils import Email


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Esto inicia sesión al usuario después de registrarse
            return redirect('home')  # Redirige al usuario a la página principal o donde desees
    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirige al home o donde quieras
    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


# class PromptFormView(FormView):
#     template_name = 'main_pages/index.html'
#     form_class = PromptForm
#     success_url = reverse_lazy('home')  # asegúrate que redirige a la raíz
#
#     def form_valid(self, form):
#
#         if self.request.user.is_authenticated:
#             prompt_text = form.cleaned_data['prompt']
#
#             user_prompt = UserPrompt.objects.create(user=self.request.user, prompt=prompt_text)
#
#             base_output_path = f"media/generated_audio/user_{self.request.user.id}_prompt_{user_prompt.id}"
#             output_path = f"{base_output_path}_huggingFace.wav"
#             ac_output_prefix = f"{base_output_path}_audioCraft"
#
#             os.makedirs(os.path.dirname(output_path), exist_ok=True)
#
#             music_service = MusicService()
#             song_title = music_service.generate_song_title(prompt_text)
#
#             print(song_title)
#
#             music_service.generate_music_audiocraft(
#                 prompts=[prompt_text],
#                 duration=8,
#                 output_prefix=ac_output_prefix
#             )
#
#             music_service.generate_music(prompt_text, output_file=output_path)
#
#             user_prompt.audio_file = output_path
#             user_prompt.save()
#
#             song_created = SongCreated.objects.create(
#                 song_name=song_title,  # nombre limitado a 100 caracteres
#                 audio_file=f"{os.path.relpath(output_path, start=settings.MEDIA_ROOT)}",  # Cambiado
#                 user=self.request.user,
#             )
#
#             html = Email.dynamic_email(song_created, 'components/music-player.html')
#             print(html)  # o úsalo como quieras
#
#             return super().form_valid(form)
#         else:
#             return redirect('login')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user_prompts'] = UserPrompt.objects.filter(user=self.request.user)
#         return context


# Clase que maneja el formulario de entrada y la creación de canciones generadas a partir de un prompt
class PromptFormView(FormView):
    template_name = 'main_pages/index.html'  # Plantilla para renderizar la página
    form_class = PromptForm  # Formulario asociado a la vista
    success_url = reverse_lazy('home')  # Redirige al home después de una acción exitosa

    def form_valid(self, form):
        """
        Procesa el formulario cuando se envía correctamente.
        Aquí se genera una canción a partir del 'prompt' ingresado por el usuario.
        """
        # Verifica si el usuario está autenticado
        if self.request.user.is_authenticated:
            # Obtiene el texto del prompt ingresado en el formulario
            prompt_text = form.cleaned_data['prompt']

            # Crea una entrada de UserPrompt para almacenar el prompt del usuario
            user_prompt = UserPrompt.objects.create(user=self.request.user, prompt=prompt_text)

            # Define las rutas donde se guardarán los archivos generados
            base_output_path = f"media/generated_audio/user_{self.request.user.id}_prompt_{user_prompt.id}"
            output_path = f"{base_output_path}_huggingFace.wav"  # Ruta para guardar la música generada por HuggingFace
            ac_output_prefix = f"{base_output_path}_audioCraft"  # Prefijo para la salida de AudioCraft

            # Asegura que el directorio de salida exista, si no, lo crea
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Inicializa el servicio de música para generar la canción
            music_service = MusicService()

            # Genera un título para la canción usando el prompt
            song_title = music_service.generate_song_title(prompt_text)
            print(song_title)  # Imprime el título generado

            # Genera la música con AudioCraft y guarda el archivo
            music_service.generate_music_audiocraft(
                prompts=[prompt_text],
                duration=8,  # Duración de la canción en segundos
                output_prefix=ac_output_prefix
            )

            # Genera la música con otro servicio y guarda el archivo en la ruta definida
            music_service.generate_music(prompt_text, output_file=output_path)

            # Asocia el archivo generado al modelo UserPrompt y guarda la entrada
            user_prompt.audio_file = output_path
            user_prompt.save()

            # Crea un registro en SongCreated para almacenar la canción generada
            song_created = SongCreated.objects.create(
                song_name=song_title,  # Título de la canción (máximo 100 caracteres)
                audio_file=f"{os.path.relpath(output_path, start=settings.MEDIA_ROOT)}",  # Ruta relativa al archivo de audio
                user=self.request.user,  # Usuario que creó la canción
            )

            # Renderiza el contenido dinámicamente.
            html = Email.dynamic_email(song_created, 'components/music-player.html')
            print(html)  # Puedes utilizar este HTML como quieras

            # Si todo es correcto, redirige a la URL de éxito
            return super().form_valid(form)
        else:
            # Si el usuario no está autenticado, redirige al login
            return redirect('login')

    def get_context_data(self, **kwargs):
        """
        Añade datos adicionales al contexto de la página, como los prompts anteriores del usuario.
        """
        context = super().get_context_data(**kwargs)
        context['user_prompts'] = UserPrompt.objects.filter(user=self.request.user)
        return context



def home(request):

    return render(request, 'main_pages/index.html')
