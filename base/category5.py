from django.http import HttpResponse
from function import *


CATEGORY = 5


def add():
    url = 'http://jobplatform.pku.edu.cn/portal/listinternship'
    for i in range(1, 3):
        r = get_page(url + '?page={0}'.format(i))
        soup = BeautifulSoup(r)
        soup = soup.find('ul', attrs={'class':'listul'})
        for i in soup.find_all('a'):
            source_url = 'http://jobplatform.pku.edu.cn' + i['href']
            add_info(source_url=source_url, category=CATEGORY)


def update(i):
    if i.category != CATEGORY:
        return
    r = get_page(i.source_url)
    soup = BeautifulSoup(r)
    soup = soup.find('ul', attrs={'class': 'wz1ul'})
    li = soup.find_all('li')
    title = li[0].text
    content = str(li[2])
    i.title = title
    i.content = content
    i.post_status = 1
    i.save()


def post(i):
    if i.category != CATEGORY:
        return
    subject = i.title[:26]
    content = str('<a href="%s" target="_blank">%s</a><div><br></div>' % (i.source_url, i.source_url)) + i.content
    try:
        res = se.get('http://www.oiegg.com/post.php?action=newthread&fid=735&gid=794&extra=page%3D1', timeout=TIMEOUT)
        if not check_oiegg_login(res.content):
            login_oiegg()
            res = se.get('http://www.oiegg.com/post.php?action=newthread&fid=735&gid=794&extra=page%3D1', timeout=TIMEOUT)
        soup = BeautifulSoup(res.content)
        soup = soup.find('form', attrs={'id': 'postform'})
        formhash = soup.find('input', attrs={'id': 'formhash'})['value']
        action = 'http://www.oiegg.com/' + soup['action']
        form = {'formhash': formhash,
                'frombbs': '1',
                'typeid': '916',
                'subject': subject,
                'message': content,
                'wysiwyg': '0',
                'htmlon': '1',
                'usesig': '1',
                'topicsubmit': 'true'}
        res = se.post(action, form, timeout=TIMEOUT)
    except Exception, e:
        logger.error(e)
    else:
        if 'tid' in res.url:
            i.post_url = res.url
            i.save()
        else:
            logger.error('unknown reason for "{0}"'.format(i.source_url))