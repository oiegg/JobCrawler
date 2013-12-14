# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from base.function import *
from base.categories import *


def addHandler(request, cid):
    exec('category{0}.add()'.format(cid))


def updateHandler(request):
    i = Info.objects.filter(post_status=0).order_by('add_time')
    if not i:
        return
    i = i[0]
    exec('category{0}.update(i)'.format(i.category))
    if i.content.count('，') < 3:
        i.post_status = 5
        i.save()
    return HttpResponse(i.source_url)
