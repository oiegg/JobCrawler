from django.http import HttpResponse
from django.shortcuts import render
from base.categories import *
from base.function import *


def indexHandler(request):
    pass


def postStatusHandler(request, status):
    res = []
    order = 'add_time'
    if status == 2:
        order = 'post_time'
    i = Info.objects.filter(post_status=status).order_by(order)
    for j in i[:8]:
        k = {}
        for p in ['title', 'source_url', 'post_url', 'category', 'post_status', 'retry']:
            k[p] = getattr(j, p)
        k['add_time'] = str(j.add_time)
        if j.post_time:
            k['post_time'] = str(j.post_time)
        else:
            k['post_time'] = None
        res.append(k)
    return HttpResponse(json.dumps(res))