"""
The upload.py file ...
"""
import requests
from lxml import html
from typing import Dict

def fetch_wiki_data(pageid: str) -> Dict:    
    response = requests.get(
    'https://en.wikipedia.org/w/api.php',
    params={
        'action': 'parse',
        'format': 'json',
        'pageid': pageid,
        'prop': 'text',
        'redirects':''
    }).json()
    raw_html = response['parse']['text']['*']
    title = response['parse']['title']
    document = html.document_fromstring(raw_html)

    text = ''
    for p in document.xpath('//p'):
        text += p.text_content() + '\n'

    return {"content": text, "partition_name": f'{title}:{pageid}'}
