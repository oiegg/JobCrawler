from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login
from base.categories import *
from base.function import *


def indexHandler(request):
    val = {}
    return render_to_response('inspector/index.html', val)


def loginHandler(request):
    u = request.GET.get('username')
    p = request.GET.get('password')
    if u and p:
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('/inspector/admin')
    val = {}
    return render_to_response('inspector/login.html', val)


def adminHandler(request):
    if request.user.is_authenticated():
        val = {}
        i = Info.objects.filter(post_status=1)
        if i:
            l = len(i)
            i = i[random.randint(0, l - 1)]
            val['info'] = i
            val['source_url'] = urllib.quote_plus(i.source_url)
        else:
            val['message'] = 'No un-posted! Fantastic!'
        return render_to_response('inspector/admin.html', val)
    else:
        return redirect('/inspector/login')


def postStatusHandler(request, status):
    res = {}
    status = int(status)
    res['status'] = status
    order = '-add_time'
    if status == 2:
        order = '-post_time'
    li = []
    i = Info.objects.filter(post_status=status).order_by(order)
    res['total'] = len(i)
    for j in i[:8]:
        li.append(j.toDict())
    res['info'] = li
    return HttpResponse(json.dumps(res))


# def infoFilterHandler(request):
#     res = {}
#     res['machine'] = 'inspector'
#     source_url = request.GET.get('source_url')
#     q = Info.objects.all()
#     if source_url:
#         q = q.filter(source_url=source_url)
#     res['total'] = len(q)
#     li = []
#     for i in q[:8]:
#         li.append(i.toDict(withContent=True))
#     res['info'] = li
#     return HttpResponse(json.dumps(res))