from django.shortcuts import render
from django.http import HttpResponse
from base.function import *
from base import category1
from base import category2


def addHandler(request, cid):
    exec('category{0}.add()'.format(cid))


def updateHandler(request):
    i = Info.objects.filter(post_status=0).order_by('add_time')
    if not i:
        return
    i = i[0]
    exec('category{0}.update(i)'.format(i.category))
    return HttpResponse(i.source_url)
