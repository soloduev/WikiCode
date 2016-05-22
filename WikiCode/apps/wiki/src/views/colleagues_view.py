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

from WikiCode.apps.wiki.models import User, Colleague
from WikiCode.apps.wiki.src.views.error_view import get_error_page
from WikiCode.apps.wiki.src.wiki_tree import WikiTree
from .auth import check_auth, get_user_id


def get_colleagues(request):
    user_data = check_auth(request)
    try:
        user = User.objects.get(email=user_data)
        wt = WikiTree(user.id_user)
        wt.load_tree(user.tree)
        # Получаем дерево сохраненных публикаций
        swt = WikiTree(user.id_user)
        swt.load_tree(user.saved_publ)

        # Получаем список коллег и их никнеймы с почтой
        colleagues = []
        colleagues_list = Colleague.objects.filter(user=user)
        for colleague in colleagues_list:
            # Получаем пользователя коллегу
            user_colleague = User.objects.get(id_user=colleague.id_colleague)

            colleagues.append({"nickname":user_colleague.nickname,
                               "email":user_colleague.email,
                               "is_favorite":colleague.is_favorite,
                               "id":colleague.id_colleague})

        user_id = get_user_id(request)
        context = {
            "user_data": user_data,
            "user_id": user_id,
            "preview_tree": wt.generate_html_preview(),
            "saved_publ": swt.generate_html_preview(),
            "colleagues":colleagues,
        }

        return render(request, 'wiki/colleagues.html', context)
    except User.DoesNotExist:
        return get_error_page(request, ["Sorry, user is not defined!", "Page not found: 'user/" + str(id) + "/'"])


@csrf_protect
def get_add_colleague(request):
    """Ajax представление. Добавляет коллегу."""
    if request.method == "POST":
        nickname = request.POST['nickname']

        # Получаем пользователя
        try:
            cur_user = User.objects.get(id_user=get_user_id(request))

            # Получаем по nickname пользователя, которого котим добавить
            add_user = User.objects.get(nickname=nickname)

            if add_user.id_user != cur_user.id_user:
                # Проверяем, есть ли уже этот коллега в списке пользователей
                try:
                    colleague = Colleague.objects.get(user=cur_user, id_colleague=add_user.id_user)
                    # Коллега есть, не добавляем
                    return HttpResponse('no', content_type='text/html')
                except Colleague.DoesNotExist:
                    # Коллеги нет, добавляем
                    new_colleague = Colleague(user=cur_user,
                                              id_colleague=add_user.id_user,
                                              is_favorite=False)
                    new_colleague.save()
                    # Добавляем коллеги с другой стороны
                    new_colleague_2 = Colleague(user=add_user,
                                                id_colleague=cur_user.id_user,
                                                is_favorite=False)
                    new_colleague_2.save()
                    return HttpResponse('ok', content_type='text/html')
            else:
                return HttpResponse('no', content_type='text/html')
        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_remove_colleague(request):
    """Ajax представление. Убирает коллегу."""
    if request.method == "POST":
        id = int(request.POST['id'])

        # Получаем пользователя
        try:
            cur_user = User.objects.get(id_user=get_user_id(request))

            # Получаем по id пользователя, которого хотим убрать
            del_user = User.objects.get(id_user=id)

            if del_user.id_user != cur_user.id_user:

                # Проверяем, есть ли уже этот коллега в списке пользователей
                try:
                    # Коллега с одной и с другой стороны
                    colleague = Colleague.objects.get(user=cur_user, id_colleague=del_user.id_user)
                    colleague_2 = Colleague.objects.get(user=del_user, id_colleague=cur_user.id_user)
                    # Коллега есть, удаляем
                    colleague.delete()
                    colleague_2.delete()
                    return HttpResponse('ok', content_type='text/html')
                except Colleague.DoesNotExist:
                    # Коллеги нет, не удаляем
                    return HttpResponse('no', content_type='text/html')
            else:
                return HttpResponse('no', content_type='text/html')
        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')

