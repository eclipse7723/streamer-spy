import json
import os
from src.manager import get_recognizer, get_speech_to_text_class


def main(params, recognizer_id, speech_to_text_id):
    recognizer = get_recognizer(recognizer_id, params["lang"])

    extra_params = {
        "twitch_url": params.get("url", "")
    }
    Worker = get_speech_to_text_class(speech_to_text_id)
    worker = Worker(recognizer, **extra_params)

    worker.run()


if __name__ == "__main__":
    with open(os.path.join(os.getcwd(), "data.json"), "r", encoding="utf-8") as f:
        data_params = json.load(f)
    main(data_params, "vosk", data_params.get("speech_to_text", "twitch"))
