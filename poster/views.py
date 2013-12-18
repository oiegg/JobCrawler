from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from base.function import *
from base.categories import *
from django.contrib.auth import authenticate, login


def postHandler(request):
    if not request.user.is_authenticated():
        return redirect('/inspector/login')
    res = {}
    res['machine'] = 'Poster'
    g = G.objects.get()
    if g.POSTER_STATUS == 0:
        i = Info.objects.filter(post_status=1).order_by('add_time')
        source_url = request.GET.get('source_url')
        if source_url:
            i = i.filter(source_url=source_url)
        target_status = request.GET.get('status')
        if not source_url:
            target_status = None
        if i:
            i = i[0]
            if target_status:
                i.post_status = target_status
                i.save()
            else:
                exec('category{0}.post(i)'.format(i.category))
            if source_url:
                val = {}
                val['info'] = i
                return render_to_response('poster/redirect.html', val)
            res['info'] = [i.toDict(), ]
    return HttpResponse(json.dumps(res))