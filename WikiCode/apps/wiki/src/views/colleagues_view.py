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

from WikiCode.apps.wiki.models import User, Colleague
from WikiCode.apps.wiki.src.views.error_view import get_error_page
from WikiCode.apps.wiki.src.views import notifications_view
from WikiCode.apps.wiki.src.modules.wiki_tree.wiki_tree import WikiFileTree
from .auth import check_auth, get_user_id


def get_colleagues(request):
    user_data = check_auth(request)
    try:
        user = User.objects.get(email=user_data)
        wft = WikiFileTree()
        wft.load_tree(user.file_tree)

        # Получаем все коллег пользователя
        colleagues = []
        try:
            all_colleagues = Colleague.objects.filter(id_user=user.id_user)

            for colleague in reversed(all_colleagues):
                try:
                    colleague_user = User.objects.get(id_user=colleague.id_colleague)
                    colleagues.append({
                        "id_user": colleague.id_user,
                        "id_colleague": colleague.id_colleague,
                        "nickname": colleague_user.nickname
                    })
                except User.DoesNotExist:
                    pass

        except Colleague.DoesNotExist:
            pass

        user_id = get_user_id(request)
        context = {
            "user_data": user_data,
            "user_id": user_id,
            "preview_tree": wft.to_html_preview(),
            "colleagues": colleagues
        }

        return render(request, 'wiki/colleagues.html', context)
    except User.DoesNotExist:
        return get_error_page(request, ["Sorry, user is not defined!"])


def get_add_colleague(request, id):
    user_data = check_auth(request)
    try:
        cur_user = User.objects.get(email=user_data)
        add_user = User.objects.get(id_user=int(id))

        try:
            Colleague.objects.get(id_user=cur_user.id_user)

            return notifications_view.get_notifications(request,
                                                        notify={'type': 'error',
                                                                'text': 'Данный пользователь у вас уже в коллегах\n\n\n'})

        except Colleague.DoesNotExist:

            new_colleague = Colleague(id_user=cur_user.id_user,
                                      id_colleague=add_user.id_user)

            new_colleague_reverse = Colleague(id_user=add_user.id_user,
                                              id_colleague=cur_user.id_user)

            new_colleague.save()
            new_colleague_reverse.save()

            return notifications_view.get_notifications(request, notify={'type': 'info',
                                                                         'text': 'Пользователь был успешно добавлен в коллеги.\n\n\n'})
    except User.DoesNotExist:
        return get_error_page(request, ["Sorry, user is not defined!"])