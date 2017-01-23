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


# Управление уведомлениями

from WikiCode.apps.wiki.models import User
from WikiCode.apps.wiki.src.views.auth import get_user_id


def momental_notify(request, type: str, message: str):
    """ Порождает моментальное уведомление для текущего пользователя.
    type:       'error' | 'info'
    message:    'any text'
    """
    try:
        user = User.objects.get(id_user=get_user_id(request))
        user.notify_text = message
        user.notify_type = type
        user.save()
    except User.DoesNotExist:
        print("User not found")
