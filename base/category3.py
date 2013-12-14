from django.http import HttpResponse
from function import *


CATEGORY = 3


def add():
    url = 'http://www.gaoxiaojob.com/zhaopin/total/'
    r = get_page(url)
    soup = BeautifulSoup(r)
    soup = soup.find('div', attrs={'class': 'listbox'})
    d = soup.find('div', attrs={'class': 'titles'})
    p = 'http://www.gaoxiaojob.com' + d.find('a')['href']
    r = get_page(p)
    soup = BeautifulSoup(r)
    soup = soup.find('div', attrs={'class': 'content'})
    soup = soup.find('table').find('td')
    a = soup.find_all('a')
    for i in a:
        source_url = i['href']
        add_info(source_url=source_url, category=CATEGORY)


def update(i):
    if i.category != CATEGORY:
        return
    r = get_page(i.source_url)
    soup = BeautifulSoup(r)
    for s in soup.find_all('script'):
        s.replace_with('')
    soup = soup.find('div', attrs={'class': 'viewbox'})
    title = soup.find('div', attrs={'class': 'title'}).text
    title = title.strip()
    soup = soup.find('div', attrs={'class': 'content'})
    content = str(soup.find('table'))
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
    subject = i.title[:26]
    content = str('<a href="%s" target="_blank">%s</a><div><br></div>' % (i.source_url, i.source_url)) + i.content
    try:
        s = requests.session()
        res = s.post('http://www.oiegg.com/logging.php?action=login', login_form, timeout=TIMEOUT)
        res = s.get('http://www.oiegg.com/post.php?action=newthread&fid=101&gid=794&extra=page%3D1', timeout=TIMEOUT)
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
        res = s.post(action, form, timeout=TIMEOUT)
    except Exception, e:
        print e
        i.retry += 1
        i.post_status = 1
        i.save()
    else:
        if 'tid' not in res.url:
            i.post_status = 4
            i.save()
            return
        i.post_url = res.url
        i.post_time = datetime.now()
        i.save()