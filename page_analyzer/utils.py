from urllib.parse import urlparse

import validators


def validate_url(url):
    if validators.url(url):
        return False
    return True


def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_scheme = parsed_url.scheme.lower()
    normalized_host = parsed_url.hostname.lower()
    return f"{normalized_scheme}://{normalized_host}"
