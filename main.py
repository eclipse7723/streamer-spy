import json
import os
from src.manager import get_recognizer, get_speech_to_text_class
from src.signals import NLPKeywordsDetector, play_sound_on_found


def main(params, recognizer_id, speech_to_text_id):
    recognizer = get_recognizer(recognizer_id, params["lang"], params["models"])

    extra_params = {
        "twitch_url": params.get("url", "")
    }
    Worker = get_speech_to_text_class(speech_to_text_id)
    worker = Worker(recognizer, **extra_params)

    if params.get("signal"):
        keywords = params["signal"].get("keywords", [])
        detector = NLPKeywordsDetector(keywords, params["lang"])

        worker.add_signal(detector, cb_true=detector.report)

        if params["signal"].get("path_to_sound"):
            path_to_sound = os.path.join(os.getcwd(), params["signal"]["path_to_sound"])
            sound_reporter = play_sound_on_found(path_to_sound)   # returns actual callback
            worker.add_signal(detector, cb_true=sound_reporter)

    worker.run()


if __name__ == "__main__":
    with open(os.path.join(os.getcwd(), "data.json"), "r", encoding="utf-8") as f:
        data_params = json.load(f)
    main(data_params, "vosk", data_params.get("speech_to_text", "twitch"))
