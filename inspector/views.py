from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from base.categories import *
from base.function import *


def indexHandler(request):
    val = {}
    return render_to_response('inspector/index.html', val)


def postStatusHandler(request, status):
    res = {}
    res['status'] = status
    order = 'add_time'
    if status == 2:
        order = 'post_time'
    li = []
    i = Info.objects.filter(post_status=status).order_by(order)
    res['total'] = len(i)
    for j in i[:8]:
        k = {}
        for p in ['title', 'source_url', 'post_url', 'category', 'post_status', 'retry']:
            k[p] = getattr(j, p)
        k['add_time'] = str(j.add_time)
        if j.post_time:
            k['post_time'] = str(j.post_time)
        else:
            k['post_time'] = None
        li.append(k)
    res['recent'] = li
    return HttpResponse(json.dumps(res))