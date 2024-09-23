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
