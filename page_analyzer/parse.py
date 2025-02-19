from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def url_parse(url):
    parse_result = urlparse(url)
    return f"{parse_result.scheme}://{parse_result.netloc}"


def seo_analysis(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return
    status_code = response.status_code
    response.encoding= 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    h1 = soup.find("h1")
    if h1:
        h1 = h1.text
    title = soup.find("title")
    if title:
        title = title.text
    description = soup.find('meta', {'name': 'description'})
    if description:
        description = description.get('content')
    return {
        "status_code": status_code,
        "h1": h1,
        "title": title,
        "description": description
        }
