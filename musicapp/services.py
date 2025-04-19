from transformers import pipeline
import scipy.io.wavfile
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write


class MusicService:
    def __init__(self):
        self.synthesiser = pipeline("text-to-audio", model="facebook/musicgen-small")
        self.model = MusicGen.get_pretrained("facebook/musicgen-small")
        self.model.set_generation_params(duration=8)
        self.generator = pipeline("text-generation", model="gpt2")

    def generate_song_title(self, prompt: str):
        title = self.generator(f"Generate a song title for: '{prompt}' without any explanation, no context, no extra words, no suggest, just the title.", max_new_tokens=10)
        return title[0]['generated_text'].strip()

    def generate_music(self, prompt: str, output_file: str = "musicgen_out.wav"):
        music = self.synthesiser(prompt, forward_params={"do_sample": True})
        scipy.io.wavfile.write(output_file, rate=music["sampling_rate"], data=music["audio"])

    def generate_music_audiocraft(self,prompts: list[str],duration: int = 8,output_prefix: str = "musicgen_audiocraft_track"):

        self.model.set_generation_params(duration=duration)
        wav_outputs = self.model.generate(prompts)

        for idx, one_wav in enumerate(wav_outputs):
            filename = f"{output_prefix}_{idx}.wav"
            audio_write(filename, one_wav.cpu(), self.model.sample_rate, strategy="loudness")