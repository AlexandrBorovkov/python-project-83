import requests
from bs4 import BeautifulSoup


def seo_analysis(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    h1_tag = soup.find("h1")
    title_tag = soup.find("title")
    description_tag = soup.find('meta', {'name': 'description'})
    return {
        "status_code": response.status_code,
        "h1": h1_tag.text[:255] if h1_tag else "",
        "title": title_tag.text[:255] if title_tag else "",
        "description": (description_tag.get('content', '')[:255]
                             if description_tag else '')
    }

