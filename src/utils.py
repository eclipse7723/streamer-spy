import sys
import wave
from io import BytesIO
from numpy import int16
from pyaudio import paInt16
from pydub import AudioSegment
from pydub.exceptions import CouldntEncodeError
from pydub.playback import play


def play_audio_segment(audio_segment):
    raw = BytesIO(audio_segment)
    try:
        raw_wav = AudioSegment.from_raw(
            raw,
            sample_width=AudioParams.segment_length,
            frame_rate=AudioParams.rate,
            channels=AudioParams.channels
        )
        play(raw_wav)
    except CouldntEncodeError as e:
        print(f"[!] play_audio_segment could not decode: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[!] play_audio_segment - unexpected error: {e}", file=sys.stderr)
        return False
    return True


def save_audio_to_file(self, audio_data, file_path="output.wav"):
    # segment_length - Для 16-битного аудио используем 2 байта
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.segment_length)
        wf.setframerate(self.rate)
        wf.writeframes(audio_data)


class AudioParams:
    rate = 16000
    channels = 1
    segment_length = 2
    twitch_audio_dtype = int16
    pyaudio_audio_format = paInt16
    frames_per_buffer = 8000
    playback_audio = False


class Colors:
    red = "\u001b[31m"
    yellow = "\u001b[33m"
    green = "\u001b[32m"
    reset = "\u001b[0m"
