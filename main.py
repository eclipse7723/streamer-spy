import sys
import numpy as np
from io import BytesIO
from pydub import AudioSegment
from pydub.exceptions import CouldntEncodeError
from twitchrealtimehandler import TwitchAudioGrabber
from src.recognizers.vosk import vosk_speech
from src.recognizers.googleapi import api_speech as googleapi_speech


recognizers = {
    "vosk": vosk_speech,
    "google": googleapi_speech,
}


class TwitchSpeechToText:
    twitch_url = ""
    audio_grabber = None
    recognizer = None
    rate = 16000
    channels = 1
    segment_length = 2

    def __init__(self, twitch_url, recognizer_id):
        self.twitch_url = twitch_url
        self.audio_grabber = TwitchAudioGrabber(
            twitch_url=twitch_url,
            dtype=np.int16,
            segment_length=self.segment_length,
            channels=self.channels,
            rate=self.rate,
        )
        if recognizer_id not in recognizers:
            raise ValueError(f"unknown {recognizer_id=}, possible values: {recognizers.keys()}")
        self.recognizer = recognizers[recognizer_id]

    def run(self):
        while True:
            audio_segment = self.audio_grabber.grab_raw()
            if not audio_segment:
                continue

            raw = BytesIO(audio_segment)
            try:
                raw_wav = AudioSegment.from_raw(
                    raw, sample_width=self.segment_length, frame_rate=self.rate, channels=self.channels
                )
            except CouldntEncodeError as e:
                print(f"[!] AudioSegment.from_raw could not decode: {e}", file=sys.stderr)
                continue

            raw_flac = BytesIO()
            raw_wav.export(raw_flac, format="flac")
            data = raw_flac.read()
            transcript = self.recognizer(data)
            print("> ", transcript)


def main(twitch_url, recognizer_id, lang):
    worker = TwitchSpeechToText(twitch_url, recognizer_id)

    if recognizer_id == "vosk":
        from src.recognizers.vosk import VoskRecognizerManager
        path_to_model = VoskRecognizerManager.MODELS[lang]
        VoskRecognizerManager.create(path_to_model, TwitchSpeechToText.rate)

    worker.run()


if __name__ == "__main__":
    main("https://www.twitch.tv/simyton", "vosk", "ua")
