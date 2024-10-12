import vosk
import json

from src.recognizers.base import BaseRecognizer


class VoskRecognizerManager:
    recognizer = None

    @staticmethod
    def get():
        """ returns VoskRecognizer or None, if not created yet"""
        return VoskRecognizerManager.recognizer

    @staticmethod
    def create(path_to_model: str, rate: int) -> None:
        if VoskRecognizerManager.recognizer is not None:
            raise Exception("already created")
        vosk_recognizer = VoskRecognizer()
        vosk_recognizer.setup(path_to_model, rate)
        VoskRecognizerManager.recognizer = vosk_recognizer


class VoskRecognizer(BaseRecognizer):
    """ vosk recognizer based on vosk.KaldiRecognizer """

    def __init__(self):
        self._model = None
        self._rec = None

    def setup(self, path_to_model: str, rate: int = 16000):
        if self._model is not None:
            raise Exception("already setup")
        self._model = vosk.Model(path_to_model)
        self._rec = vosk.KaldiRecognizer(self._model, rate)

    def recognize(self, data) -> str | None:
        if self._rec.AcceptWaveform(data):
            result = json.loads(self._rec.Result())
            return result['text']


def vosk_speech(data) -> str | None:
    vosk_recognizer = VoskRecognizerManager.get()
    if vosk_recognizer is None:
        raise TypeError("init vosk recognizer first with VoskRecognizerManager.create(...)")
    result = vosk_recognizer.recognize(data)
    return result
