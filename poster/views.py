from django.http import HttpResponse
from django.shortcuts import render
from base.function import *
from base.categories import *


def postHandler(request):
    if g.POSTER_STATUS == 0:
        i = Info.objects.filter(post_status=1).order_by('add_time')
        if not i:
            return
        i = i[0]
        exec('category{0}.post(i)'.format(i.category))
        return HttpResponse(i.post_url)