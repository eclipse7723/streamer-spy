## Install

1. Клонировать репозиторий:

```
git clone https://github.com/eclipse7723/streamer-spy
```

2. Установить зависимости

```
pip install -r requirements.txt
```

3. Скачать `ffmpeg` и прописать его в `PATH`

4. Скачать модели в папку **models** с сайта https://alphacephei.com/vosk/models:

```
streamer-spy
    > models
        > vosk-model-small-ru-0.22
        > vosk-model-small-uk-v3-small
    > src
    main.py
    models.json
    ...
```

5. Вписать пути к ним через `data.json`, указать язык и ссылку на пользователя:

```json
{
  "models": {
    "ru": "streamer-spy/models/vosk-model-small-ru-0.22",
    "ua": "streamer-spy/models/vosk-model-small-uk-v3-small"
  },
  "lang": "ua",
  "url": "https://www.twitch.tv/..."
}
```

6. Запустить `main.py`

## Сигналы

Можно добавить к шпиону возможность тригериться на какие-то ключевые слова с помощью такого кода:

```python
from src.signals import simply_detect_keywords
from src.speech.twitch import TwitchSpeechToText
from src.recognizers.vosk import vosk_speech

def report_if_keyword_found(text):
    print(f"Bad word detected: {text}.")

keywords = {"пиздец", "сука", "блять", "блядь"}

worker = TwitchSpeechToText(vosk_speech, twitch_url="...")
worker.add_signal(
    lambda text: simply_detect_keywords(text, keywords),
    cb_true=report_if_keyword_found
)
worker.run()
```

Можно добавить любой свой сигнал. Функция должна принимать 1 аргумент - входной текст.
При добавлении сигнала необходимо определить хотя бы 1 калбек (`cb_true`, `cb_false`).