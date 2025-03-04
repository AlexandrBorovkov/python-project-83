from urllib.parse import urlparse

import validators


def validate_url(input_url):
    if not input_url:
        return "URL обязателен для заполнения"
    if not validators.url(input_url):
        return "Некорректный URL"
    if len(input_url) > 255:
        return "Введенный URL превышает длину в 255 символов"


def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_scheme = parsed_url.scheme.lower()
    normalized_host = parsed_url.hostname.lower()
    return f"{normalized_scheme}://{normalized_host}"
