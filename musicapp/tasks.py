"""Background generation.

Generating eight seconds of audio takes minutes on CPU and loads models worth
hundreds of megabytes. That cannot happen inside an HTTP request, so the view
queues this task and returns immediately; the browser polls for the result.
"""

import os

from celery import shared_task
from django.conf import settings

from musicapp.models import SongCreated, UserPrompt
from musicapp.services import get_music_service


@shared_task(bind=True)
def generate_song(self, user_prompt_id: int):
    """Generate a track for an existing UserPrompt and record the result."""
    user_prompt = UserPrompt.objects.select_related("user").get(pk=user_prompt_id)
    prompt_text = user_prompt.prompt

    output_path = os.path.join(
        settings.MEDIA_ROOT,
        "generated_audio",
        f"user_{user_prompt.user_id}_prompt_{user_prompt.id}.wav",
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    service = get_music_service()

    self.update_state(state="PROGRESS", meta={"step": "title"})
    song_title = service.generate_song_title(prompt_text)

    self.update_state(state="PROGRESS", meta={"step": "audio"})
    service.generate_music(prompt_text, output_file=output_path)

    relative_path = os.path.relpath(output_path, start=settings.MEDIA_ROOT).replace(
        "\\", "/"
    )

    # UserPrompt has no audio_file field; SongCreated is what holds the result.
    song = SongCreated.objects.create(
        song_name=song_title,
        audio_file=relative_path,
        user=user_prompt.user,
    )

    return {"song_id": song.id, "title": song_title, "audio": relative_path}
