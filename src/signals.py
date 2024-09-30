import os
import threading
from nltk.stem import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk import download
from pydub import AudioSegment
from pydub.playback import play
from src.utils import ua_stopwords, Colors

download('stopwords')


def _tokenize(text):
    # we always get input without punctuation and with lower case, so no need to use nltk.tokenize.word_tokenize
    return text.split(" ")


_stemmers = {
    "en": PorterStemmer(),
    "ru": SnowballStemmer("russian"),
    "ua": SnowballStemmer("russian"),
}

_stopwords = {
    "en": stopwords.words("english"),
    "ua": ua_stopwords,
    "ru": stopwords.words("russian"),
}


def check_keywords(words: set, keywords: set):
    """ Returns True if at least 1 keyword is in the words array """
    if keywords & words:
        return True
    return False


class KeywordsDetectorInterface:
    def __call__(self, text: str) -> bool:
        raise NotImplementedError

    def report(self, text: str) -> str:
        raise NotImplementedError


class SimpleKeywordsDetector(KeywordsDetectorInterface):
    def __init__(self, keywords):
        if len(keywords) == 0:
            raise ValueError("No keywords provided")
        self.keywords = set(keywords)
        print(f"{Colors.yellow}Listen to next exactly keywords: {Colors.green}{', '.join(self.keywords)}{Colors.reset}")

    def __call__(self, text: str):
        words = set(_tokenize(text))
        detected_words = self.keywords & words
        return len(detected_words) > 0

    def report(self, text: str):
        t = ""
        for word in text.split():
            if word in self.keywords:
                t += f"{Colors.red}{word} "
            else:
                t += f"{Colors.yellow}{word} "
        print(f"{Colors.green}Keywords detected: {Colors.yellow}{t}{Colors.reset}")


class NLPKeywordsDetector(KeywordsDetectorInterface):
    def __init__(self, keywords: set, lang="en"):
        if len(keywords) == 0:
            raise ValueError("No keywords provided")
        if lang not in _stemmers or lang not in _stopwords:
            raise ValueError(f"Unknown language: {lang}")

        self.keywords = self.prepare_keywords(keywords, lang)
        print(f"{Colors.yellow}Listen to next {Colors.green}{lang}{Colors.yellow} stemmed keywords: "
              f"{Colors.green}{', '.join(self.keywords)}{Colors.reset}")

        self.stemmer = _stemmers[lang]
        self.stopwords = _stopwords[lang]
        self.last_detected_words = []

    def __call__(self, text: str):
        # stem each word and exclude stopwords
        words = set(self.stemmer.stem(word) for word in _tokenize(text) if word not in self.stopwords)
        detected_words = self.keywords & words

        # save default words to highlight them in report
        self.last_detected_words = [word for word in _tokenize(text) if self.stemmer.stem(word) in detected_words]

        return len(detected_words) > 0

    def report(self, text: str):
        t = ""
        for word in text.split():
            if word in self.last_detected_words:
                t += f"{Colors.red}{word} "
            else:
                t += f"{Colors.yellow}{word} "
        print(f"{Colors.green}Keywords detected: {Colors.yellow}{t}{Colors.reset}")

    @staticmethod
    def prepare_keywords(keywords, lang="en"):
        if lang not in _stemmers:
            raise ValueError(f"Unknown language: {lang}")
        stemmer = _stemmers[lang]
        new_keywords = set(stemmer.stem(word) for word in keywords)
        return new_keywords


def play_sound_on_found(path_to_sound):
    file_name, file_extension = os.path.splitext(path_to_sound)
    if file_extension == "wav":
        audio_fragment = AudioSegment.from_wav(path_to_sound)
    elif file_extension == "mp3":
        audio_fragment = AudioSegment.from_mp3(path_to_sound)
    else:
        raise ValueError(f"Unknown file extension: {file_extension}, only wav or mp3")

    def wrapper(text):
        threading.Thread(target=play, args=(audio_fragment,)).start()
    return wrapper
