"""
The upload.py file ...
"""
import requests
from lxml import html
from typing import Dict

def fetch_wiki_data(title: str) -> Dict:    
    response = requests.get(
    'https://en.wikipedia.org/w/api.php',
    params={
        'action': 'parse',
        'format': 'json',
        'page': title,
        'prop': 'text',
        'redirects':''
    }).json()
    raw_html = response['parse']['text']['*']
    pageid = response['parse']['pageid']
    document = html.document_fromstring(raw_html)

    text = ''
    for p in document.xpath('//p'):
        stopwords = ['is', 'a', 'at', 'is', 'the']
        querytext = p.text_content().split()

        result  = [word for word in querytext if word.lower() not in stopwords]
        text += ' '.join(result)

    return {"content": text, "partition_name": f'{title}:{pageid}'}
