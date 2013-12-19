# coding=utf-8
from bs4 import BeautifulSoup
import requests
from models import *
from datetime import datetime
import re
import json
import logging
import random
import urllib


logger = logging.getLogger(__name__)
logger.info('Logger Start!')


TIMEOUT = 16
MAX_RETRY = 8
se = requests.session()


def check_oiegg_login(page):
    soup = BeautifulSoup(page)
    soup = soup.find('div', attrs={'id': 'menu'})
    if 'pm.php' in str(soup):
        return True
    return False


def login_oiegg():
    for i in range(0, MAX_RETRY):
        g = G.objects.get()
        login_form = {'referer': '/',
                      'cookietime': '2592000',
                      'username': g.OIEGG_USERNAME,
                      'password': g.OIEGG_PASSWORD,
                      'loginsubmit': '登录'}
        se.post('http://www.oiegg.com/logging.php?action=login', login_form, timeout=TIMEOUT)
        if check_oiegg_login(se.get('http://www.oiegg.com/index.php').content):
            logger.info('Login succeeded!')
            return
    logger.error('Login failed!')


def get_page(url):
    for i in range(0, 3):
        try:
            res = requests.get(url=url, timeout=TIMEOUT)
        except Exception, e:
            logger.error(e)
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