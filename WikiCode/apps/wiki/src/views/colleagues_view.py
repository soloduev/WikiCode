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

from WikiCode.apps.wiki.models import User, Colleague, Notification
from WikiCode.apps.wiki.src.modules.wiki_tree.wiki_tree import WikiFileTree
from WikiCode.apps.wiki.src.engine import wcode
from .auth import check_auth, get_user_id


def get_colleagues(request):
    """ Возвращает страницу списка коллег пользователя."""

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
            "colleagues": colleagues,
            "notify": wcode.notify.instant.get(request)
        }

        return render(request, 'wiki/colleagues.html', context)
    except User.DoesNotExist:
        return wcode.goerror(request, ["Sorry, user is not defined!"])


def get_add_colleague(request, id):
    user_data = check_auth(request)
    try:
        cur_user = User.objects.get(email=user_data)
        add_user = User.objects.get(id_user=int(id))

        try:
            Colleague.objects.get(id_user=cur_user.id_user)
            wcode.notify.instant.create(request, 'error', 'Данный пользователь у вас уже в коллегах\n\n\n')
            return wcode.goto('notifications')

        except Colleague.DoesNotExist:

            new_colleague = Colleague(id_user=cur_user.id_user,
                                      id_colleague=add_user.id_user)

            new_colleague_reverse = Colleague(id_user=add_user.id_user,
                                              id_colleague=cur_user.id_user)

            # Когда мы добавляем коллегу, удаляем заявки, если они есть у пользователей
            Notification.objects.filter(id_addressee=cur_user.id_user,
                                        id_sender=add_user.id_user,
                                        type="add_colleague").delete()

            Notification.objects.filter(id_addressee=add_user.id_user,
                                        id_sender=cur_user.id_user,
                                        type="add_colleague").delete()

            new_colleague.save()
            new_colleague_reverse.save()

            wcode.notify.instant.create(request, 'info', 'Пользователь был успешно добавлен в коллеги.\n\n\n')
            return wcode.goto('notifications')

    except User.DoesNotExist:
        return wcode.goerror(request, ["Sorry, user is not defined!"])


def get_delete_colleague(request):
    if request.method == "POST":
        try:
            cur_user = User.objects.get(id_user=get_user_id(request))
            del_user_id = User.objects.get(id_user=request.POST.get("delete_colleague_id"))

            try:
                colleague = Colleague.objects.get(id_user=cur_user.id_user, id_colleague=del_user_id.id_user)
                colleague_reverse = Colleague.objects.get(id_user=del_user_id.id_user, id_colleague=cur_user.id_user)
                colleague.delete()
                colleague_reverse.delete()

                wcode.notify.instant.create(request, 'info', 'Пользователь был успешно убран из Вашего списка коллег.\n\n')
                return wcode.goto('colleagues')

            except Colleague.DoesNotExist:
                wcode.notify.instant.create(request, 'error', 'Извините, но этот коллега уже был удален из вашего списка.\n\n')
                return wcode.goto('colleagues')

        except User.DoesNotExist:
            return wcode.goerror(request, ["Sorry, user is not defined!"])
    else:
        return wcode.goerror(request, ["Извините, но удалить этого пользователя из Вашего списка коллег, пока невозможно. Приносим свои извинения."])