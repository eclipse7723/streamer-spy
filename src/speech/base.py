import time


class BaseSpeechToText:
    def __init__(self, recognizer):
        self.recognizer = recognizer
        self.signals = {}

    def run(self):
        raise NotImplementedError()

    def process_result(self, text):
        if not text:
            return
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {text!r}")
        self.process_signals(text)

    def process_signals(self, text):
        for signal, callbacks in self.signals.items():
            if signal(text):
                for (cb_true, cb_false) in callbacks:
                    if cb_true:
                        cb_true(text)
            else:
                for (cb_true, cb_false) in callbacks:
                    if cb_false:
                        cb_false(text)

    def add_signal(self, signal, cb_true=None, cb_false=None):
        if not callable(cb_true) and not callable(cb_false):
            raise ValueError("at least one of cb_true or cb_false should be a function")
        self.signals.setdefault(signal, []).append((cb_true, cb_false))
        print(f"[+] Signal added")
