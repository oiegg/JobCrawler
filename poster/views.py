from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from base.function import *
from base.categories import *
from django.contrib.auth import authenticate, login


def postHandler(request):
    res = {}
    res['machine'] = 'Poster'
    g = G.objects.get()
    if g.POSTER_STATUS == 0:
        i = Info.objects.filter(post_status=1).order_by('add_time')
        source_url = request.GET.get('source_url')
        if source_url:
            i = i.filter(source_url=source_url)
        if i:
            i = i[0]
            i.retry += 1
            if i.retry > MAX_RETRY:
                i.post_status = 3
                i.save()
            else:
                i.post_status = 2
                i.save()
                exec('category{0}.post(i)'.format(i.category))
                if source_url:
                    val = {}
                    if i.post_url:
                        i.post_time = datetime.now()
                        i.save()
                        val['message'] = 'Successfully posted @ <a href={0}>{0}</a>'.format(i.post_url)
                    else:
                        i.post_status = 1
                        i.save()
                        val['message'] = 'Post failed!'
                    return render_to_response('poster/redirect.html', val)
                res['info'] = [i.toDict(), ]
    return HttpResponse(json.dumps(res))


def deleteHandler(request):
    if not request.user.is_authenticated():
        return redirect('/inspector/login')
    res = {}
    res['machine'] = 'Poster'
    source_url = request.GET.get('source_url')
    if source_url:
        i = Info.objects.filter(source_url=source_url)
        if i:
            i = i[0]
            i.post_status = 6
            i.save()
            val = {}
            val['message'] = 'Abandoned!'
    return render_to_response('poster/redirect.html', val)