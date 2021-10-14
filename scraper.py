from json import load, dump
from typing import Dict, List
from bs4 import BeautifulSoup
from requests import get

def scrape() -> Dict[str, List]:
    page = get('http://kaomoji.ru/en', headers = {
            "accept": "text/html",
            "accept-language": "en-GB,en-US;q=1",
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "0",
            "User-Agent": "Safari/537.36"
        })
    page.encoding = 'utf-8'

    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup.prettify())

    tag = soup.find('h2', string='Japanese Emoticons: Positive Emotions')

    kaomoji = {}

    while True:
        tag = tag.find_next('h3')
        if tag is None:
            break
        emotion = tag.findChild().string.lower()
        # print(emotion)
        
        items = []
        for item in tag.find_next('table', {'class': 'table_kaomoji'}).findChildren('span'):
            kaomoji_from_span = item.string
            if kaomoji_from_span is not None:
                items.append(kaomoji_from_span)
        
        kaomoji[emotion] = items

    return kaomoji

def enrich_downloaded_dict(filename: str, input_dict: Dict) -> Dict[str, List]:
    with open(filename, 'r', encoding='utf8') as file:
        file_dict = load(file, encoding='utf-8')
    
    changed = False
    for key in input_dict:
        if key not in file_dict:
            changed = True
            file_dict[key] = input_dict[key]
        else:
            for item in input_dict[key]:
                if item not in file_dict[key]:
                    changed = True
                    file_dict[key].append(item)

    if changed:
        with open(filename, 'w', encoding='utf-8') as file:
            dump(file_dict, file, indent=4, ensure_ascii=False)

    return file_dict

if __name__ == '__main__':
    dict = scrape()
    dict = enrich_downloaded_dict('kaomoji.json', dict)