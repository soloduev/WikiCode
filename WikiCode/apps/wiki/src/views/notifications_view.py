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
import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from WikiCode.apps.wiki.models import User, Colleague, Notification, CommentBlock, Publication, Comment
from WikiCode.apps.wiki.src.views.error_view import get_error_page
from WikiCode.apps.wiki.src.wiki_tree import WikiTree
from .auth import check_auth, get_user_id


def get_notifications(request):
    user_data = check_auth(request)
    try:
        user = User.objects.get(email=user_data)
        wt = WikiTree(user.id_user)
        wt.load_tree(user.tree)
        # Получаем дерево сохраненных публикаций
        swt = WikiTree(user.id_user)
        swt.load_tree(user.saved_publ)

        # Получаем все уведомления
        notifications_list = Notification.objects.filter(user=user, is_delete=False)

        notifications = []
        number = 1

        for notification in reversed(notifications_list):
            try:
                # Получаем никнейм пользователя, отправившего уведомление
                user_sender = User.objects.get(id_user=notification.id_author)
                notifications.append({
                    "number":number,
                    "nickname":user_sender.nickname,
                    "id":user_sender.id_user,
                    "date":notification.date,
                    "user":notification.user,
                    "type":notification.type,
                    "message":notification.message,
                    "message_answer":notification.message_answer,
                    "is_read":notification.is_read,
                    "is_delete":notification.is_delete})
                number = number+1

            except User.DoesNotExist:
                print("Пользователя отправившего это уведомление не существует")

        user_id = get_user_id(request)
        context = {
            "user_data": user_data,
            "user_id": user_id,
            "preview_tree": wt.generate_html_preview(),
            "saved_publ": swt.generate_html_preview(),
            "notifications": notifications
        }

        return render(request, 'wiki/notifications.html', context)
    except User.DoesNotExist:
        return get_error_page(request, ["Sorry, user is not defined!", "Page not found: 'user/" + str(id) + "/'"])


@csrf_protect
def get_remove_notification(request):
    """Ajax представление. Удаление уведомления"""
    if request.method == "POST":
        nickname = request.POST.get('nickname')
        date = request.POST.get('date')

        try:
            # Получаем текущего пользователя
            cur_user = User.objects.get(id_user=get_user_id(request))

            # Получаем пользователя отправившего уведомление
            add_user = User.objects.get(nickname=nickname)

            # Получаем уведомление
            try:
                notification = Notification.objects.get(user=cur_user, id_author=add_user.id_user, date=date)
                # Удаляем его
                notification.delete()
                return HttpResponse('ok', content_type='text/html')
            except Notification.DoesNotExist:
                # Уведомления не существует
                return HttpResponse('no', content_type='text/html')
        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_send_request_for_colleagues(request):
    """Ajax представление. Отправляет запрос на добавление в коллеги"""
    if request.method == "POST":
        nickname = request.POST['nickname']

        # Получаем пользователя
        try:

            cur_user = User.objects.get(id_user=get_user_id(request))

            # Получаем по nickname пользователя, которого хотим добавить
            add_user = User.objects.get(nickname=nickname)

            if add_user.id_user != cur_user.id_user:
                # Проверяем, есть ли уже этот коллега в списке пользователей
                try:
                    colleague = Colleague.objects.get(user=cur_user, id_colleague=add_user.id_user)
                    # Коллега есть, не отправляем запрос
                    return HttpResponse('no', content_type='text/html')
                except Colleague.DoesNotExist:
                    # Коллеги нет, отправляем запрос на добавление в коллеги

                    # Последняя проверка, не отправляли ли мы уже заявку
                    try:
                        check_notification = Notification.objects.get(user=add_user,
                                                                  id_author=cur_user.id_user,
                                                                  type="invite_colleagues",
                                                                  is_read=False)
                        print("Вы уже отправляли ему заявку")
                        return HttpResponse('no', content_type='text/html')
                    except Notification.DoesNotExist:
                        # Выполняем запрос

                        # Получаем текущую дату
                        date = str(datetime.datetime.now())
                        date = date[:len(date) - 7]

                        new_notification = Notification(user=add_user,
                                                        id_author=cur_user.id_user,
                                                        type="invite_colleagues",
                                                        message="User "+str(cur_user.nickname)+" invite "+str(add_user.nickname),
                                                        message_answer="",
                                                        date=date,
                                                        is_read=False,
                                                        is_delete=False)

                        new_notification.save()
                        print("Заявка в коллеги отправлена")
                        return HttpResponse('ok', content_type='text/html')
            else:
                return HttpResponse('no', content_type='text/html')
        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_read_notification(request):
    """Ajax представление. Делает уведомление прочитанным"""

    if request.method == "POST":
        nickname = request.POST.get('nickname')
        date = request.POST.get('date')


        try:
            # Получаем текущего пользователя
            cur_user = User.objects.get(id_user=get_user_id(request))

            # Получаем пользователя отправившего уведомление
            add_user = User.objects.get(nickname=nickname)

            # Получаем уведомление
            try:
                notification = Notification.objects.get(user=cur_user,id_author=add_user.id_user,date=date)
                # Уведомление получено
                notification.is_read = True
                notification.save()
                return HttpResponse('ok', content_type='text/html')
            except Notification.DoesNotExist:
                # Уведомления не существует
                return HttpResponse('no', content_type='text/html')
        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_user_send_message(request, id):
    """Ajax представление. Отправляет письмо пользователю"""

    if request.method == "POST":
        message = request.POST.get('message')

        try:
            # Получаем текущего пользователя
            cur_user = User.objects.get(id_user=get_user_id(request))

            # Получаем пользователя который должен получить уведомление
            get_user = User.objects.get(id_user=id)

            # Получаем текущую дату
            date = str(datetime.datetime.now())
            date = date[:len(date) - 7]

            send_notification = Notification(user=get_user,
                                            id_author=cur_user.id_user,
                                            type="message",
                                            message=message,
                                            message_answer="",
                                            date=date,
                                            is_read=False,
                                            is_delete=False)

            sended_notification = Notification(user=cur_user,
                                             id_author=get_user.id_user,
                                             type="sended message",
                                             message=message,
                                             message_answer="",
                                             date=date,
                                             is_read=True,
                                             is_delete=False)
            sended_notification.save()
            send_notification.save()
            print("Письмо отправлено")
            return HttpResponse('ok', content_type='text/html')

        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_colleague_send_message(request):
    """Ajax представление. Отправляет письмо пользователю с экрана коллег"""

    if request.method == "POST":
        message = request.POST.get('message')
        id = int(request.POST.get('id'))

        try:
            # Получаем текущего пользователя
            cur_user = User.objects.get(id_user=get_user_id(request))

            # Получаем пользователя который должен получить уведомление
            get_user = User.objects.get(id_user=id)

            # Получаем текущую дату
            date = str(datetime.datetime.now())
            date = date[:len(date) - 7]

            send_notification = Notification(user=get_user,
                                             id_author=cur_user.id_user,
                                             type="message",
                                             message=message,
                                             message_answer="",
                                             date=date,
                                             is_read=False,
                                             is_delete=False)

            sended_notification = Notification(user=cur_user,
                                               id_author=get_user.id_user,
                                               type="sended message",
                                               message=message,
                                               message_answer="",
                                               date=date,
                                               is_read=True,
                                               is_delete=False)
            sended_notification.save()
            send_notification.save()
            print("Письмо отправлено")
            return HttpResponse('ok', content_type='text/html')

        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_send_answer_message(request):
    """Ajax представление. Отвечает на письмо."""

    if request.method == "POST":
        message = request.POST.get('message')
        nickname = request.POST.get('nickname')
        answer = request.POST.get('answer')

        try:
            # Получаем текущего пользователя
            cur_user = User.objects.get(id_user=get_user_id(request))

            # Получаем пользователя который должен получить уведомление
            get_user = User.objects.get(nickname=nickname)

            # Получаем текущую дату
            date = str(datetime.datetime.now())
            date = date[:len(date) - 7]

            send_notification = Notification(user=get_user,
                                             id_author=cur_user.id_user,
                                             type="answer message",
                                             message=answer,
                                             message_answer=message,
                                             date=date,
                                             is_read=False,
                                             is_delete=False)

            sended_notification = Notification(user=cur_user,
                                               id_author=get_user.id_user,
                                               type="sended message",
                                               message=answer,
                                               message_answer=message,
                                               date=date,
                                               is_read=True,
                                               is_delete=False)
            sended_notification.save()
            send_notification.save()
            print("Ответ отправлен")
            return HttpResponse('ok', content_type='text/html')

        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_send_answer_comment(request, id):
    """Ajax представление. Отвечает на общий комментарий в конспекте."""

    if request.method == "POST":
        text = request.POST.get('text')
        nickname = request.POST.get('nickname')
        answer = request.POST.get('answer')

        try:
            # Получаем текущего пользователя
            cur_user = User.objects.get(id_user=get_user_id(request))

            # Получаем пользователя который должен получить уведомление
            get_user = User.objects.get(nickname=nickname)

            # Получаем текущую дату
            date = str(datetime.datetime.now())
            date = date[:len(date) - 7]

            # Создаем уведомление
            send_notification = Notification(user=get_user,
                                             id_author=cur_user.id_user,
                                             type="answer comment",
                                             message=answer,
                                             message_answer=text,
                                             date=date,
                                             is_read=False,
                                             is_delete=False)

            # Далее, создаем новый комментарий в публикации
            comment_block = CommentBlock.objects.get(id_publication=id)
            publication = Publication.objects.get(id_publication=id)

            # Обновляем статистику пользователей
            cur_user.comments += 1
            get_user.commented_it += 1
            # Получаем пользователя конспекта
            user_publ = User.objects.get(id_user=publication.id_author)
            user_publ.commented_it += 1

            # Создаем новый комментарий
            new_comment = Comment(comment_block=comment_block,
                                  num_position=comment_block.last_id + 1,
                                  id_author=cur_user.id_user,
                                  nickname_author=cur_user.nickname,
                                  rating=0,
                                  text=get_user.nickname+", "+answer,
                                  data=date,
                                  id_author_answer=get_user.id_user,
                                  nickname_author_answer=get_user.nickname)

            # Сохраняем все изменения в БД
            new_comment.save()
            comment_block.last_id += 1
            comment_block.save()
            cur_user.save()
            get_user.save()
            user_publ.save()
            send_notification.save()
            print("Ответ на общий комментарий отправлен")
            return HttpResponse('ok', content_type='text/html')

        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')
        except CommentBlock.DoesNotExist:
            return get_error_page(request, ["This is comment block not found!"])
        except Publication.DoesNotExist:
            return get_error_page(request, ["This is publication not found!"])

    else:
        return HttpResponse('no', content_type='text/html')
