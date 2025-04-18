from transformers import pipeline
import scipy.io.wavfile

class MusicService:
    def __init__(self):
        self.synthesiser = pipeline("text-to-audio", model="facebook/musicgen-small")

    def generate_music(self, prompt: str, output_file: str = "musicgen_out.wav"):
        # Usamos el pipeline para generar la música a partir del prompt.
        music = self.synthesiser(prompt, forward_params={"do_sample": True})
        # Guardamos el archivo de música generado.
        scipy.io.wavfile.write(output_file, rate=music["sampling_rate"], data=music["audio"])
