from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from base.function import *
from base.categories import *


def postHandler(request):
    res = {}
    res['machine'] = 'Poster'
    if g.POSTER_STATUS == 0:
        i = Info.objects.filter(post_status=1).order_by('add_time')
        source_url = request.GET.get('source_url')
        if source_url:
            i = i.filter(source_url=source_url)
        if i:
            i = i[0]
            exec('category{0}.post(i)'.format(i.category))
            if source_url:
                val = {}
                val['info'] = i
                return render_to_response('poster/redirect.html', val)
            res['info'] = [i.toDict(), ]
    return HttpResponse(json.dumps(res))