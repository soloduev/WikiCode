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

from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.contrib.auth.models import User as DjangoUser
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from WikiCode.apps.wiki.models import Publication
from WikiCode.apps.wiki.models import Statistics
from WikiCode.apps.wiki.models import Colleague
from WikiCode.apps.wiki.models import Notification
from WikiCode.apps.wiki.models import User
from WikiCode.apps.wiki.models import User as WikiUser
from WikiCode.apps.wiki.src.modules.wiki_tree.wiki_tree import WikiFileTree
from WikiCode.apps.wiki.src.views.error_view import get_error_page
from WikiCode.apps.wiki.src.views.index_view import get_index
from .auth import check_auth, get_user_id


def get_user(request, id, notify=None):
    """ Возвращает страницу пользователя.
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
    try:
        user = User.objects.get(email=user_data)
        if str(get_user_id(request)) == id:
            # Отрисовываем страницу текущего пользователя

            wft = WikiFileTree()
            wft.load_tree(user.file_tree)

            user_id = get_user_id(request)
            # Получаем текст превью публикации
            try:
                preview_publ = Publication.objects.get(id_publication=user.preview_publ_id)
                preview_publ_text = preview_publ.text
                prewiew_publ_title = preview_publ.title
                prewiew_publ_id = preview_publ.id_publication
            except Publication.DoesNotExist:
                preview_publ_text = None
                prewiew_publ_title = None
                prewiew_publ_id = None

            if user_id != -1:
                context = {
                    "user_data": user_data,
                    "user_id": user_id,
                    "preview_tree": wft.to_html_preview(),
                    "user":user,
                    "prewiew_publ_text":preview_publ_text,
                    "prewiew_publ_title":prewiew_publ_title,
                    "prewiew_publ_id":prewiew_publ_id,
                    "other_user": False,
                    "new_notifications": Notification.objects.filter(id_addressee=user.id_user, is_read=False).count(),
                    "total_colleagues": Colleague.objects.filter(id_user=user.id_user).count(),
                    "notify": notify
                }

                return render(request, 'wiki/user.html', context)
            else:
                return get_error_page(request, ["Sorry, id user problem!", "Page not found: 'user/" + str(id) + "/'"])
        else:
            # Отрисовываем страницу другого пользователя
            other_user = User.objects.get(id_user=id)
            wft = WikiFileTree()
            wft.load_tree(other_user.file_tree)

            # Узнаем, не является ли он коллегой
            is_colleague = False
            try:
                Colleague.objects.get(id_user=get_user_id(request),
                                      id_colleague=other_user.id_user)
                is_colleague = True
            except Colleague.DoesNotExist:
                pass

            # Узнаем, не отправляли ли мы ему уже заявку в коллеги
            is_send_colleague = False
            if Notification.objects.filter(id_addressee=other_user.id_user,
                                           id_sender=get_user_id(request),
                                           type="add_colleague").count() != 0:
                is_send_colleague = True


            # Получаем текст превью публикации
            try:
                preview_publ = Publication.objects.get(id_publication=other_user.preview_publ_id)
                preview_publ_text = preview_publ.text
                prewiew_publ_title = preview_publ.title
                prewiew_publ_id = preview_publ.id_publication
            except Publication.DoesNotExist:
                preview_publ_text = None
                prewiew_publ_title = None
                prewiew_publ_id = None

            context = {
                "user_data": user_data,
                "user_id": get_user_id(request),
                "preview_tree": wft.to_html_preview(),
                "user":other_user,
                "prewiew_publ_text": preview_publ_text,
                "prewiew_publ_title": prewiew_publ_title,
                "prewiew_publ_id": prewiew_publ_id,
                "other_user": True,
                "is_colleague": is_colleague,
                "is_send_colleague": is_send_colleague,
                "notify": notify
            }

            return render(request, 'wiki/user.html', context)

    except User.DoesNotExist:
        return get_error_page(request, ["Sorry, user is not defined!","Page not found: 'user/"+str(id)+"/'"])


def get_create_user(request):
    """Регистрация нового пользователя"""

    # Получаем данные формы
    form = request.POST

    # Проверяем на существование такого имени и email.
    # Осли проверка успешна, пользователя не создаем
    try:
            simple1 = WikiUser.objects.get(nickname=form["user_nickname"])
    except WikiUser.DoesNotExist:
        try:
            simple2 = WikiUser.objects.get(email=form["user_email"])
        except WikiUser.DoesNotExist:

            # Создаем нового пользователя
            user = DjangoUser.objects.create_user(form["user_nickname"],
                                                  form["user_email"],
                                                  form["user_password"])

            stat = Statistics.objects.get(id_statistics=1)
            # Необходимо для создания id пользователей
            total_reg_users = stat.users_total_reg
            stat.users_total_reg += 1
            stat.users_reg += 1

            # Создаем дерево по умолчанию для юзера
            wft = WikiFileTree()
            wft.create_tree(total_reg_users)

            # Создаем нового юзера
            new_wiki_user = WikiUser(user=user,
                                     nickname=form["user_nickname"],
                                     email=form["user_email"],
                                     id_user=total_reg_users,
                                     tree="",
                                     file_tree=wft.get_xml_str(),
                                     avatar="none.jpg",
                                     name="anonymous",
                                     publications=0,
                                     preview_publ_id=-1)

            user = authenticate(username=form["user_nickname"], password=form["user_password"])

            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    print(">>>>>>>>>>>>>> WIKI ERROR: disabled account")

            else:
                print(">>>>>>>>>>>>>> WIKI ERROR: invalid login")


            # Сохранение всех изменений в БД
            new_wiki_user.save()
            stat.save()

            return HttpResponseRedirect("/")
        context = {
            "error": "Пользователь с таким Email уже существует",
            "user_data": check_auth(request),
            "user_id": get_user_id(request),
        }
        return render(request, 'wiki/registration.html', context)
    context = {
        "error": "Пользователь с таким Nickname уже существует",
        "user_data": check_auth(request),
        "user_id": get_user_id(request),
    }
    return render(request, 'wiki/registration.html', context)


def get_login_user(request):

    user_name = request.POST['user_name']
    user_password = request.POST['user_password']

    user = authenticate(username=user_name, password=user_password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return get_index(request, notify={'text': 'Авторизация прошла успешно.',
                                              'type': 'info'})
        else:
            print(">>>>>>>>>>>>>> WIKI ERROR: disabled account")
            return get_index(request)

    else:
        print(">>>>>>>>>>>>>> WIKI ERROR: invalid login")

    return get_index(request, notify={'text': 'Вы ввели не верный логин или пароль!\n\n\nПовторите снова.', 'type': 'error'})


def get_logout_user(request):

    logout(request)
    return HttpResponseRedirect("/")


@csrf_protect
def get_login(request):

    context = {
        "user_data": check_auth(request),
        "user_id": get_user_id(request),
    }

    return render(request, 'wiki/login.html', context)
