import validators


def validate(data):
    url = data.get("url")
    if validators.url(url):
        return True
    return False
