import requests
import json

url = "https://translate.argosopentech.com/translate"


def translate(payload):
    response = requests.post(url, json=payload)
    json_response = response.text

    parsed_response = json.loads(json_response)

    translated_text = parsed_response["translatedText"]
    return translated_text


def to_en(message):
    payload = {
        "q": message,
        "source": "ru",
        "target": "en",
        "format": "text",
        "api_key": "",
    }
    result = translate(payload)
    return result


def to_ru(message):
    payload = {
        "q": message,
        "source": "en",
        "target": "ru",
        "format": "text",
        "api_key": "",
    }
    result = translate(payload)
    return result
