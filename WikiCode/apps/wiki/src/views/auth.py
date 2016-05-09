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



from WikiCode.apps.wiki.models import User

def check_auth(request):
    """Проверка аутентифицирован ли пользователь"""
    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    return user_data


def get_user_id(request):
    user_data = check_auth(request)
    id_user = -1;
    try:
        if user_data != "None":
            user = User.objects.get(email=user_data)
            id_user = user.id_user
        return id_user
    except User.DoesNotExist:
        return -1;