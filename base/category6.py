from django.http import HttpResponse
from function import *


CATEGORY = 6


def add():
    url = 'http://jobplatform.pku.edu.cn/portal/listinternship'
    for i in range(1, 3):
        p = 'http://career.ruc.edu.cn/Article_Class2.asp?ClassID=39&SpecialID=0&page=' + str(i)
        r = get_page(p)
        soup = BeautifulSoup(r)
        soup = soup.find_all('a', attrs={'class': 'STYLE8'})
        for i in soup:
            source_url = 'http://career.ruc.edu.cn/' + i['href']
            add_info(source_url=source_url, category=CATEGORY)


def update(i):
    if i.category != CATEGORY:
        return
    r = get_page(i.source_url)
    r = r.decode('gbk')
    r = r[r.find('<body>') + 6:r.rfind('</body>')]
    soup = BeautifulSoup(r)
    t = soup.find_all('table')
    t[len(t) - 2].extract()
    t[0].extract()
    title = soup.find('strong').text
    st = 0
    for j in soup.find_all():
        if st > 0:
            content = str(j)
            break
        if j.name == 'img':
            st = 1
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