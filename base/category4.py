from django.http import HttpResponse
from function import *


CATEGORY = 4


def add():
    url = 'http://career.bnu.edu.cn/JobInfomation.aspx?catid=472'
    r = get_page(url)
    soup = BeautifulSoup(r)
    soup = soup.find('dl', attrs={'class': 'ji120101'})
    a = soup.find_all('a')
    for i in a:
        source_url = 'http://career.bnu.edu.cn/' + i['href']
        add_info(source_url=source_url, category=CATEGORY)


def update(i):
    if i.category != CATEGORY:
        return
    r = get_page(i.source_url)
    soup = BeautifulSoup(r)
    soup = soup.find('dl', attrs={'class': 'intro02'})
    title = soup.find('dt').text
    title = title.split(' ')[0]
    content = str(soup.find('dd'))
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
        s = requests.session()
        s.post('http://www.oiegg.com/logging.php?action=login', login_form, timeout=TIMEOUT)
        res = s.get('http://www.oiegg.com/post.php?action=newthread&fid=735&gid=794&extra=page%3D1', timeout=TIMEOUT)
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
        res = s.post(action, form, timeout=TIMEOUT)
    except Exception, e:
        logger.error(e)
    else:
        if 'tid' in res.url:
            i.post_url = res.url
            i.save()
