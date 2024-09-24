import time
import re
from twitchrealtimehandler import TwitchAudioGrabber
from src.speech.base import BaseSpeechToText
from src.utils import play_audio_segment, AudioParams


class TwitchSpeechToText(BaseSpeechToText):
    twitch_url = ""
    audio_grabber = None
    recognizer = None

    def __init__(self, recognizer, twitch_url, **kwargs):
        super().__init__(recognizer)

        if not re.match(r"https?://(www\.)?twitch\.tv/(.+)", twitch_url):
            raise ValueError(f"Bad twitch url: {twitch_url}")
        self.twitch_url = twitch_url

    def connect(self):
        print(f"Connect to {self.twitch_url}...")
        self.audio_grabber = TwitchAudioGrabber(
            twitch_url=self.twitch_url,
            dtype=AudioParams.twitch_audio_dtype,
            segment_length=AudioParams.segment_length,
            channels=AudioParams.channels,
            rate=AudioParams.rate,
        )

    def run(self):
        try:
            self.connect()
        except ValueError as e:
            print(f"may be streamer {self.twitch_url} is offline")
            raise e

        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Begin to recognize twitch streamer audio...")
        print(f"[*] Recognizing will start in a few seconds. Twitch knows you're not watching from its website.")
        while True:
            audio_segment = self.audio_grabber.grab_raw()
            if not audio_segment:
                continue

            if AudioParams.playback_audio:
                play_audio_segment(audio_segment)

            result = self.recognizer(audio_segment)
            self.process_result(result)
