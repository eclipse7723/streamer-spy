from src.speech.twitch import TwitchSpeechToText
from src.speech.mine import MineSpeechToText
from src.recognizers.vosk import vosk_speech, VoskRecognizerManager
from src.recognizers.googleapi import api_speech as googleapi_speech
from src.utils import AudioParams


recognizers = {
    "vosk": vosk_speech,
    "google": googleapi_speech,
}
speech_to_text_classes = {
    "twitch": TwitchSpeechToText,
    "mine": MineSpeechToText,
}


def get_recognizer(recognizer_id, lang):
    if recognizer_id not in recognizers:
        raise ValueError(f"unknown {recognizer_id=}, possible values: {recognizers.keys()}")
    recognizer = recognizers[recognizer_id]

    if recognizer_id == "vosk":
        if lang not in VoskRecognizerManager.MODELS:
            raise ValueError(f"model for lang {lang!r} not registered in data.json at 'models' section")

        path_to_model = VoskRecognizerManager.MODELS[lang]
        VoskRecognizerManager.create(path_to_model, AudioParams.rate)

    return recognizer


def get_speech_to_text_class(speech_to_text_id):
    if speech_to_text_id not in speech_to_text_classes:
        raise ValueError(f"unknown {speech_to_text_id=}, possible values: {speech_to_text_classes.keys()}")
    return speech_to_text_classes[speech_to_text_id]
