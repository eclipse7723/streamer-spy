import json
import sys
import requests
from fake_useragent import UserAgent


ua = UserAgent()


class GoogleApiParams:
    lang = "ua"
    api_key = ""
    api_url = "http://www.google.com/speech-api/v2/recognize"    # fixme


def api_speech(data):
    """Call google api to get the transcript of an audio"""
    # Random header
    headers = {
        "Content-Type": "audio/x-flac; rate=16000;",
        "User-Agent": ua["google chrome"],
    }
    params = (
        ("client", "chromium"),
        ("pFilter", "0"),
        ("lang", GoogleApiParams.lang),
        ("key", GoogleApiParams.api_key),
    )

    proxies = None

    if len(data) == 0:
        return

    # api call
    try:
        response = requests.post(
            GoogleApiParams.api_url,
            proxies=proxies,
            headers=headers,
            params=params,
            data=data,
        )
    except Exception as exc:
        print(f"[!] api_speech POST request failed: {exc.__class__.__name__} {exc}", file=sys.stderr)
        return

    if response.status_code != 200:
        print(f"[!] api_speech request status is not 200: {response.status_code}", file=sys.stderr)\

    # Parse api response
    try:
        transcript = extract_transcript(response.text)
        return transcript
    except Exception as exc:
        print(f"[!] api_speech extract_transcript failed: {exc.__class__.__name__} {exc}", file=sys.stderr)


def extract_transcript(resp: str):
    """
    Extract the first results from google api speech recognition
    Args:
        resp: response from google api speech.
    Returns:
        The more confident prediction from the api
        or an error if the response is malformatted
    """
    try:
        response = json.loads(resp.strip("\n"))
    except Exception as exc:
        raise ValueError("Failed to proceed api response {!r}: {} {}".format(resp, exc.__class__.__name__, exc))

    if "result" not in response:
        raise ValueError("Error non valid response from api: {}".format(resp))

    try:
        out = response["result"][0]["alternative"][0]["transcript"]
        return out
    except IndexError as exc:
        raise IndexError(f"{exc} in {response}")
