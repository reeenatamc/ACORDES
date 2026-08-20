"""Wrappers around the local generation models.

The models are expensive to load (MusicGen plus GPT-2 is several hundred MB and
tens of seconds), so they are loaded lazily and kept on the module-level
singleton returned by ``get_music_service``. A Celery worker therefore pays that
cost once, on its first task, and not on every generation.

Never call this from inside a request handler. Generation takes minutes; it
belongs in ``musicapp.tasks``.

Nothing heavy is imported at module level. ``musicapp.views`` reaches this
module through ``musicapp.tasks``, so a torch import up here would load several
hundred megabytes into every web process at startup for code it never runs.
Each backend is imported inside the method that needs it.
"""

MODEL_NAME = "facebook/musicgen-small"
TITLE_MODEL_NAME = "gpt2"


class MusicService:
    """Loads each model on first use and holds it for the process lifetime."""

    def __init__(self):
        self._synthesiser = None
        self._titler = None
        self._musicgen = None

    @property
    def synthesiser(self):
        from transformers import pipeline

        if self._synthesiser is None:
            self._synthesiser = pipeline("text-to-audio", model=MODEL_NAME)
        return self._synthesiser

    @property
    def titler(self):
        from transformers import pipeline

        if self._titler is None:
            self._titler = pipeline("text-generation", model=TITLE_MODEL_NAME)
        return self._titler

    @property
    def musicgen(self):
        from audiocraft.models import MusicGen

        if self._musicgen is None:
            self._musicgen = MusicGen.get_pretrained(MODEL_NAME)
        return self._musicgen

    def generate_song_title(self, prompt: str) -> str:
        title = self.titler(
            f"Generate a song title for: '{prompt}' without any explanation, "
            "no context, no extra words, no suggest, just the title.",
            max_new_tokens=10,
        )
        return title[0]["generated_text"].strip()

    def generate_music(self, prompt: str, output_file: str) -> str:
        """Generate a track and write it to ``output_file``. Returns the path."""
        import scipy.io.wavfile

        music = self.synthesiser(prompt, forward_params={"do_sample": True})
        scipy.io.wavfile.write(output_file, rate=music["sampling_rate"], data=music["audio"])
        return output_file

    def generate_music_audiocraft(
        self, prompts: list[str], duration: int = 8, output_prefix: str = "track"
    ) -> list[str]:
        """Alternative backend via AudioCraft, with loudness normalisation.

        Not used by the default task -- kept because it produces better
        normalised audio and may replace ``generate_music`` later.
        """
        from audiocraft.data.audio import audio_write

        self.musicgen.set_generation_params(duration=duration)
        written = []
        for idx, one_wav in enumerate(self.musicgen.generate(prompts)):
            filename = f"{output_prefix}_{idx}"
            audio_write(filename, one_wav.cpu(), self.musicgen.sample_rate, strategy="loudness")
            written.append(f"{filename}.wav")
        return written


_service = None


def get_music_service() -> MusicService:
    """Return the process-wide MusicService, creating it on first call."""
    global _service
    if _service is None:
        _service = MusicService()
    return _service
