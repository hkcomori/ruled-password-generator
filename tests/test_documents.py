# -*-coding: utf-8 -*-

from urllib.request import urlopen, Request

from bs4 import BeautifulSoup
from markdown2 import Markdown


DOC_LIST = [
    'README.md',
]

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'


def get_links_from_md(file_path, markdowner=Markdown()):
    with open(file_path) as f:
        md = f.read()

        html = markdowner.convert(md)
        soup = BeautifulSoup(html, 'html.parser')
        links = {a.attrs.get('href') for a in soup.find_all('a')}
        images = {img.attrs.get('src') for img in soup.find_all('img')}
        urls = {i for j in [links, images] for i in j}
        return urls


def test_url_status():
    markdowner = Markdown()
    for d in DOC_LIST:
        for url in get_links_from_md(d, markdowner=markdowner):
            req = Request(url, headers={'User-Agent': USER_AGENT})
            try:
                res = urlopen(req)
            except Exception as e:
                raise Exception(e, url)
            assert res.status == 200
