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


# Декоратор, применив который к представлению, разрешит вход на страницу, только по паролю разработчика

from django.shortcuts import render

from WikiCode.apps.wiki.models import User, Developer
from WikiCode.apps.wiki.src.views.auth import check_auth, get_user_id
import configuration as wiki_settings


def develop_mode(view):
    def wrapper(request):
        # Проверяем, включен ли режим для разработчиков
        if wiki_settings.DEVELOP_MODE:
            user_id = get_user_id(request)
            try:
                # Получаем имя текущего пользователя
                user = User.objects.get(id_user=user_id)
                name_developer = user.nickname

                # Проверяем, входит ли он в число разработчиков
                # Если входит, разрешаем ему выполнять представление
                developers = Developer.objects.get(name_developer=name_developer)
                return view(request)
            except Developer.DoesNotExist:
                # Если НЕ входит, перенаправляем его на страницу ремонта сайта
                user_data = check_auth(request)

                context = {
                    "user_data": user_data,
                    "user_id": user_id,
                }
                return render(request, 'wiki/develop_mode.html', context)
            except User.DoesNotExist:
                # Если НЕ входит, перенаправляем его на страницу ремонта сайта
                user_data = check_auth(request)

                context = {
                    "user_data": user_data,
                    "user_id": user_id,
                }
                return render(request, 'wiki/develop_mode.html', context)
        else:
            return view(request)

    return wrapper


def develop_mode_id(view):
    def wrapper(request, id):
        # Проверяем, включен ли режим для разработчиков
        if wiki_settings.DEVELOP_MODE:
            user_id = get_user_id(request)
            try:
                # Получаем имя текущего пользователя
                user = User.objects.get(id_user=user_id)
                name_developer = user.nickname

                # Проверяем, входит ли он в число разработчиков
                # Если входит, разрешаем ему выполнять представление
                developers = Developer.objects.get(name_developer=name_developer)
                return view(request, id)
            except Developer.DoesNotExist or User.DoesNotExist:
                # Если НЕ входит, перенаправляем его на страницу ремонта сайта
                user_data = check_auth(request)

                context = {
                    "user_data": user_data,
                    "user_id": user_id,
                }
                return render(request, 'wiki/develop_mode.html', context)
            except User.DoesNotExist:
                # Если НЕ входит, перенаправляем его на страницу ремонта сайта
                user_data = check_auth(request)

                context = {
                    "user_data": user_data,
                    "user_id": user_id,
                }
                return render(request, 'wiki/develop_mode.html', context)
        else:
            return view(request, id)

    return wrapper
