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
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from WikiCode.apps.wiki.models import BugReport, User
from WikiCode.apps.wiki.src.views.auth import get_user_id, check_auth
import datetime


def get_error_page(request, errors_arr):
    context = {
            "user_data": check_auth(request),
            "user_id": get_user_id(request),
            "error": errors_arr
        }
    return render(request, 'wiki/error.html', context)


def get_bug_report(request):
    context = {
        "user_data": check_auth(request),
        "user_id": get_user_id(request),
    }
    return render(request, 'wiki/bug_report.html', context)


@csrf_protect
def get_send_bug(request):
    """Ajax представление. Отправляет баг репорт."""

    try:
        # Получаем пользователя оставившего текст
        user = User.objects.get(id_user=get_user_id(request))

        # Получаем текст сообщения о найденной ошибки
        text = request.POST.get('text')

        # Получаем текущую дату
        date = str(datetime.datetime.now())
        date = date[:len(date) - 7]

        new_bug_report = BugReport(id_author=user.id_user,
                                   nickname_author=user.nickname,
                                   name_author=user.name,
                                   date=date,
                                   text=text)
        new_bug_report.save()

        return HttpResponse('ok', content_type='text/html')
    except User.DoesNotExist:
        return HttpResponse('no', content_type='text/html')