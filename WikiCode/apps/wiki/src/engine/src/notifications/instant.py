#   # -*- coding: utf-8 -*-
#
#   Copyright (C) 2016-2017 Igor Soloduev <diahorver@gmail.com>
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


# Моментальные уведомления

from WikiCode.apps.wiki.src.engine.src import djangoapi as __djangoapi


def create(request, type: str, message: str):
    """ Порождает моментальное уведомление для текущего пользователя.
    type:       'error' | 'info'
    message:    'any text'
    """
    try:
        user = __djangoapi.User.objects.get(id_user=__djangoapi.get_user_id(request))
        user.notify_text = message
        user.notify_type = type
        user.save()
    except __djangoapi.User.DoesNotExist:
        print("User not found")


def get(request) -> str:
    """ Возвращает текущее моментальное увеодмление для пользователя в виде notify объекта. """
    try:
        result_notify = {}
        user = __djangoapi.User.objects.get(id_user=__djangoapi.get_user_id(request))
        if user.notify_text:
            result_notify['text'] = user.notify_text
            user.notify_text = ""
        if user.notify_type:
            result_notify['type'] = user.notify_type
            user.notify_type = ""
        user.save()
        return result_notify
    except __djangoapi.User.DoesNotExist:
        print("User not found")
