import time
import pyaudio
from src.utils import AudioParams, play_audio_segment


class MineSpeechToText:
    def __init__(self, recognizer, **kwargs):
        self.recognizer = recognizer
        p = pyaudio.PyAudio()
        self.stream = p.open(
            format=AudioParams.pyaudio_audio_format,
            channels=AudioParams.channels,
            rate=AudioParams.rate,
            input=True,
            frames_per_buffer=AudioParams.frames_per_buffer
        )

    def run(self):
        self.stream.start_stream()

        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Begin to recognize own audio from microphone...")
        while True:
            audio_segment = self.stream.read(AudioParams.frames_per_buffer)

            if AudioParams.playback_audio:
                play_audio_segment(audio_segment)

            result = self.recognizer(audio_segment)
            if result:
                print(f"Recognized text: {result}")
