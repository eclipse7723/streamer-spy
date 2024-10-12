import time

from src.signals import BaseSignal


class BaseSpeechToText:
    def __init__(self, recognizer: callable, **extra_params):
        self.recognizer = recognizer
        self.signals = {}

    def run(self) -> None:
        """ starts recognizing process, each time should call `process_result` """
        raise NotImplementedError()

    def process_result(self, text: str) -> None:
        """ prints recognized text and starts attached signals """
        if not text:
            return
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {text!r}")
        self.process_signals(text)

    def process_signals(self, text: str):
        """ process all attached signals and their callbacks """
        for signal, callbacks in self.signals.items():
            if signal(text):
                for (cb_true, cb_false) in callbacks:
                    if cb_true:
                        cb_true(text)
            else:
                for (cb_true, cb_false) in callbacks:
                    if cb_false:
                        cb_false(text)

    def add_signal(self, signal: BaseSignal, cb_true: callable = None, cb_false: callable = None):
        """ attaches new signal and its callbacks; possible to add many callbacks on 1 signal """
        if not callable(cb_true) and not callable(cb_false):
            raise ValueError("at least one of cb_true or cb_false should be a function")
        self.signals.setdefault(signal, []).append((cb_true, cb_false))
        print(f"[+] Signal added")
