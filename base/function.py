# coding=utf-8
from bs4 import BeautifulSoup
import requests
from models import *
from datetime import datetime


TIMEOUT = 8
MAX_RETRY = 4
g = G.objects.get()
login_form = {'referer': '/',
              'cookietime': '2592000',
              'username': g.OIEGG_USERNAME,
              'password': g.OIEGG_PASSWORD,
              'loginsubmit': '登录'}


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


def add_info(source_url, category):
    if get_info_by_source(source_url):
        return
    i = Info(source_url=source_url,
             category=category,
             add_time=datetime.now(),
             post_status=0,
             retry=0)
    i.save()