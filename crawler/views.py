# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from base.function import *
from base.categories import *


def addHandler(request, cid):
    res = {}
    res['machine'] = 'Crawler'
    if g.CRAWLER_STATUS == 0:
        exec('category{0}.add()'.format(cid))
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
            for j in ['title', 'source_url', 'category']:
                res[j] = getattr(i, j)
    return HttpResponse(json.dumps(res))
