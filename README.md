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

Можно добавить к шпиону возможность тригериться на какие-то ключевые слова с помощью 
встроенного решения `NLPKeywordsDetector` или более простого `SimpleKeywordsDetector`:

```python
from src.signals import NLPKeywordsDetector, SimpleKeywordsDetector
from src.speech.twitch import TwitchSpeechToText
from src.recognizers.vosk import vosk_speech

keywords = {"код", "промо", "промокод", "пишите", "чат"}

worker = TwitchSpeechToText(vosk_speech, twitch_url="...")
detector = NLPKeywordsDetector(keywords, "ru")
worker.add_signal(detector, cb_true=detector.report)
worker.run()
```

Можно добавить любой свой сигнал. Функция должна принимать 1 аргумент - входной текст.
При добавлении сигнала необходимо определить хотя бы 1 калбек (`cb_true`, `cb_false`).
Пример:

```python
keywords = {"кот", "собак", "лошад", "кон", "хомяк"}

def detect_keywords(text):
    words = set(text.split())
    for word in words:
        if any([word.startswith(keyword) for keyword in keywords]):
            return True
    return False

def on_found(text):
    print("Пользователь упомянул животное")

worker.add_signal(detect_keywords, cb_true=on_found)
worker.run()
```