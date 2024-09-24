import json
import os
from src.manager import get_recognizer, get_speech_to_text_class
from src.signals import simply_detect_keywords
from src.utils import Colors



class KeywordsReporter:
    def __init__(self, keywords):
        self.keywords = keywords

    def __call__(self, text):
        t = ""
        for word in text.split():
            if word in self.keywords:
                t += f"{Colors.red}{word} "
            else:
                t += f"{Colors.yellow}{word} "
        print(f"{Colors.green}Keywords detected: {Colors.yellow}{t}{Colors.reset}")


def main(params, recognizer_id, speech_to_text_id):
    recognizer = get_recognizer(recognizer_id, params["lang"])

    extra_params = {
        "twitch_url": params.get("url", "")
    }
    Worker = get_speech_to_text_class(speech_to_text_id)
    worker = Worker(recognizer, **extra_params)

    if params.get("signal"):
        keywords = set(params["signal"].get("keywords", []))
        worker.add_signal(
            lambda text: simply_detect_keywords(text, keywords),
            cb_true=KeywordsReporter(keywords)
        )

    worker.run()


if __name__ == "__main__":
    with open(os.path.join(os.getcwd(), "data.json"), "r", encoding="utf-8") as f:
        data_params = json.load(f)
    main(data_params, "vosk", data_params.get("speech_to_text", "twitch"))
