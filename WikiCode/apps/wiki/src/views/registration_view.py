#   # -*- coding: utf-8 -*-
#
#   Copyright (C) 2016 Igor Soloduev <diahorver@gmail.com>
#
#   This file is part of WikiCode.
#
#   WikiCode is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   WikiCode is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with WikiCode.  If not, see <http://www.gnu.org/licenses/>.



from .auth import check_auth, get_user_id
from django.shortcuts import render
from WikiCode.apps.wiki.models import User as WikiUser
from django.http import HttpResponse


def get_registration(request):

    context = {
        "user_data" : check_auth(request),
        "user_id": get_user_id(request),
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