from django.http import HttpResponse
from django.shortcuts import render
from base.function import *
from base import category1


def postHandler(request):
    i = Info.objects.filter(post_status=1).order_by('add_time')
    if not i:
        return
    i = i[0]
    res = ''
    exec('res = category{0}.post(i)'.format(i.category))
    return HttpResponse(res)