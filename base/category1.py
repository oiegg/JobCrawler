from django.http import HttpResponse
from function import *


CATEGORY = 1


def add():
    url = 'http://career.bnu.edu.cn/JobInfomation.aspx?catid=470'
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
    if i.retry > MAX_RETRY:
        i.post_status = 3
        i.save()
        return
    i.post_status = 2
    i.save()
    subject = i.title
    content = i.content
    try:
        s = requests.session()
        s.post('http://www.oiegg.com/logging.php?action=login', login_form)
        res = s.get('http://www.oiegg.com/post.php?action=newthread&fid=101&gid=794&extra=page%3D1')
        soup = BeautifulSoup(res.content)
        soup = soup.find('form', attrs={'id': 'postform'})
        formhash = soup.find('input', attrs={'id': 'formhash'})['value']
        action = 'http://www.oiegg.com/' + soup['action']
        form = {'formhash': formhash,
                'frombbs': '1',
                'typeid': '1',
                'subject': subject,
                'message': content,
                'wysiwyg': '0',
                'htmlon': '1',
                'usesig': '1',
                'topicsubmit': 'true'}
        res = s.post(action, form)
    except:
        i.retry += 1
        i.post_status = 1
        i.save()
    else:
        i.post_url = res.url
        i.post_time = datetime.now()
        i.save()
