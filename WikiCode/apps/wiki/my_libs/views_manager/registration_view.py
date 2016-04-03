# -*- coding: utf-8 -*-

from .auth import check_auth
from django.shortcuts import render
from WikiCode.apps.wiki.models import User as WikiUser
from django.http import HttpResponse


def get_registration(request):

    context = {
        "user_data" : check_auth(request),
    }

    return render(request, 'wiki/registration.html', context)


def get_check_nickname(request):
    """Ajax представление. Проверка на существование такого nickname в базе данных"""

    if request.method == "GET":
        request.session['nickname'] = request.GET['nickname']
        nickname = request.GET['nickname']

        try:
            user = WikiUser.objects.get(nickname=nickname)
        except WikiUser.DoesNotExist:
            if nickname.lower() == "admin":
                return HttpResponse('ok', content_type='text/html')
            else:
                return HttpResponse('no', content_type='text/html')

        return HttpResponse('ok', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')


def get_check_email(request):
    """Ajax представление. Проверка на существование такого email в базе данных"""

    if request.method == "GET":
        request.session['email'] = request.GET['email']
        email = request.GET['email']

        try:
            user = WikiUser.objects.get(email=email)
        except WikiUser.DoesNotExist:
            if email == "diahorver@gmail.com":
                return HttpResponse('ok', content_type='text/html')
            else:
                return HttpResponse('no', content_type='text/html')

        return HttpResponse('ok', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')