from bs4 import BeautifulSoup
import requests
from models import *
from datetime import datetime


TIMEOUT = 16


def get_page(url):
    for i in range(0, 3):
        try:
            res = requests.get(url=url, timeout=TIMEOUT)
        except:
            pass
        else:
            return res.content


def get_info_by_source(source_url):
    i = Info.objects.filter(source_url=source_url)
    if i:
        return i.get()


def add_info(title, content, category, source_url):
    if get_info_by_source(source_url):
        return
    i = Info(title=title,
             content=content,
             category=category,
             source_url=source_url,
             add_time=datetime.now(),
             post_status=0)
    i.save()