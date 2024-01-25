"""
The upload.py file ...
"""
import requests
from lxml import html
from typing import Dict

def fetch_wiki_data(page: str, should_filter: bool=True) -> Dict:    
    response = requests.get(
    'https://en.wikipedia.org/w/api.php',
    params={
        'action': 'parse',
        'format': 'json',
        'page': page,
        'prop': 'text',
        'redirects':''
    }).json()
    raw_html = response['parse']['text']['*']
    pageid = response['parse']['pageid']
    document = html.document_fromstring(raw_html)

    text = ''
    for p in document.xpath('//p'):
        line = p.text_content()
        if should_filter:
            stopwords = ['is', 'a', 'at', 'is', 'the']
            querytext = line.split()

            result  = [word for word in querytext if word.lower() not in stopwords]
            text += ' '.join(result)
        else:
            text += line

    return {"content": text, "partition_name": f'{page}:{pageid}'}
