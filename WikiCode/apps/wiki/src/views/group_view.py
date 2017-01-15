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
from django.shortcuts import render

from WikiCode.apps.wiki.src.views.auth import check_auth, get_user_id


def get_group(request, id, notify=None):
    """ Возвращает страницу группы.
        Может принимать notify(сообщение, которое можно вывести после отображения страницы):
        notify:
            {
                'type': 'error|info',
                'text': 'any text',
            }
    """
    if notify is None:
        notify = {'type': 'msg', 'text': ''}

    user_data = check_auth(request)

    if str(get_user_id(request)) == id:
        # Отрисовываем страницу текущего пользователя

        context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
        }

        return render(request, 'wiki/group.html', context)

    else:
        # Отрисовываем страницу другого пользователя

        context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
        }

        return render(request, 'wiki/group.html', context)


def create_group(request):

    context = {

    }

    return render(request, 'wiki/group.html', context)
