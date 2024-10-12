class BaseRecognizer:
    def recognize(self, data) -> str | None:
        raise NotImplementedError()
