import time
from twitchrealtimehandler import TwitchAudioGrabber
from src.utils import play_audio_segment
from src.utils import AudioParams


class TwitchSpeechToText:
    twitch_url = ""
    audio_grabber = None
    recognizer = None

    def __init__(self, recognizer, twitch_url, **kwargs):
        self.twitch_url = twitch_url
        self.audio_grabber = TwitchAudioGrabber(
            twitch_url=twitch_url,
            dtype=AudioParams.twitch_audio_dtype,
            segment_length=AudioParams.segment_length,
            channels=AudioParams.channels,
            rate=AudioParams.rate,
        )
        print(f"Connected to {twitch_url}...")
        self.recognizer = recognizer

    def run(self):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Begin to recognize twitch streamer audio...")
        print(f"[*] Recognizing will start in a few seconds. Twitch knows your not watching from its website.")
        while True:
            audio_segment = self.audio_grabber.grab_raw()
            if not audio_segment:
                continue

            if AudioParams.playback_audio:
                play_audio_segment(audio_segment)

            transcript = self.recognizer(audio_segment)
            if transcript:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {transcript!r}")
