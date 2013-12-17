# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from base.function import *
from base.categories import *


def addHandler(request, cid=None):
    res = {}
    res['machine'] = 'Crawler'
    if g.CRAWLER_STATUS == 0:
        if cid:
            exec('category{0}.add()'.format(cid))
        else:
            cid = 1
            while True:
                try:
                    exec('category{0}.add()'.format(cid))
                except NameError:
                    break
                cid += 1
    return HttpResponse(json.dumps(res))


def updateHandler(request):
    res = {}
    res['machine'] = 'Crawler'
    if g.CRAWLER_STATUS == 0:
        i = Info.objects.filter(post_status=0).order_by('add_time')
        if i:
            i = i[0]
            exec('category{0}.update(i)'.format(i.category))
            if i.content.count('，') < 3:
                i.post_status = 5
                i.save()
            res['info'] = [i.toDict(), ]
    return HttpResponse(json.dumps(res))
