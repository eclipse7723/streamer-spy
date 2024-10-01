## Install

1. Clone repository:

```
git clone https://github.com/eclipse7723/streamer-spy
```

2. Install requirements:

```
pip install -r requirements.txt
```

3. Download [ffmpeg](https://www.ffmpeg.org/download.html) and add it to the `PATH`.

4. Put [vosk](https://alphacephei.com/vosk/models) **models** to the `models/` folder:

```
streamer-spy
    > models/
        > vosk-model-small-ru-0.22
        > vosk-model-small-uk-v3-small
    > res/
    > src/
    main.py
    data.json
    ...
```

5. Add the path to the models in `data.json` like this (where key is `lang`, value is `path`):

```json
{
  "models": {
    "ru": "streamer-spy/models/vosk-model-small-ru-0.22",
    "ua": "streamer-spy/models/vosk-model-small-uk-v3-small"
  },
  ...
}
```

6. Set the `lang` in `data.json` and `url` for twitch live stream.

7. Run `main.py` or `start.bat` (automatically creates venv and installs requirements).

## Signals

You can add ability to the spy to trigger on given keywords using `.add_signal()`
 with built-in `src.signals.NLPKeywordsDetector` (ignores stopwords and use 
stemming technics) or simple `src.signals.SimpleKeywordsDetector` (exact match):

```python
from src.signals import NLPKeywordsDetector, SimpleKeywordsDetector
from src.speech.twitch import TwitchSpeechToText
from src.recognizers.vosk import vosk_speech

keywords = {"code", "promo", "promocode", "write", "chat"}

worker = TwitchSpeechToText(vosk_speech, twitch_url="...")
detector = NLPKeywordsDetector(keywords, "en")
worker.add_signal(detector, cb_true=detector.report)
worker.run()
```

You can create your own signals. Function must take 1 argument - the input text.
Also, you need to implement at least 1 callback (`cb_true` if keyword found or `cb_false` if not).
Example:

```python
keywords = {"cat", "dog", "hors", "hamster", "kitt"}

def detect_keywords(text):
    words = set(text.split())
    for word in words:
        if any([word.startswith(keyword) for keyword in keywords]):
            return True
    return False

def on_found(text):
    print("User mentioned an animal")

worker.add_signal(detect_keywords, cb_true=on_found)
worker.run()
```

## `data.json` structure

* `models` - contains vosk models info inside:
  * {`<lang>`: `<path_to_vosk_model>`}
* `speech_to_text` - audio source. Possible values: `"twitch"` _(default)_, `"mine"` (from users microphone)
* `lang` - language of given speech
* `url` - url to the twitch live stream
* `signal` - contains params of signal
  * `keywords` - list of keywords that will trigger app (prints message with highlighted words)
  * `path_to_sound` - path to the sound that will be played after the keyword found (**.wav** or **.mp3**)
    * You can use built-in sound located in `res/keyword_found.wav`