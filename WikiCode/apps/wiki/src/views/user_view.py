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
import random
import configuration

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.contrib.auth.models import User as DjangoUser
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from WikiCode.apps.wiki.manager import wcode_manager
from WikiCode.apps.wiki.models import Developer
from WikiCode.apps.wiki.models import InviteKeys
from WikiCode.apps.wiki.models import RegistrationKey
from WikiCode.apps.wiki.models import Publication
from WikiCode.apps.wiki.models import Statistics
from WikiCode.apps.wiki.models import User
from WikiCode.apps.wiki.models import User as WikiUser
from WikiCode.apps.wiki.src.engine import wcode
from WikiCode.apps.wiki.src.fs.fs import WikiFileSystem
from .auth import check_auth, get_user_id


class EmailAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = DjangoUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            DjangoUser().set_password(password)

    def get_user(self, user_id):
        try:
            return DjangoUser.objects.get(pk=user_id)
        except DjangoUser.DoesNotExist:
            return None


def get_user(request, id):
    """ Возвращает страницу пользователя."""

    user_data = check_auth(request)
    try:
        user = User.objects.get(email=user_data)

        if str(get_user_id(request)) == id:
            # Отрисовываем страницу текущего пользователя

            if not user.is_activated:
                return wcode.goerror(request,
                                     ["Sorry, user is not defined!", "Page not found: 'user/" + str(id) + "/'"])

            wft = WikiFileSystem()
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

            # Получаем все последние конспекты пользователя
            publications = Publication.objects.filter(id_author=id)

            if user_id != -1:
                context = {
                    "user_data": user_data,
                    "user_id": user_id,
                    "preview_tree": wft.to_html_preview(),
                    "publications": reversed(publications),
                    "user": user,
                    "prewiew_publ_text": preview_publ_text,
                    "prewiew_publ_title": prewiew_publ_title,
                    "prewiew_publ_id": prewiew_publ_id,
                    "other_user": False,
                }

                return render(request, 'wiki/user.html', context)
            else:
                return wcode.goerror(request, ["Sorry, id user problem!", "Page not found: 'user/" + str(id) + "/'"])
        else:
            # Отрисовываем страницу другого пользователя
            other_user = User.objects.get(id_user=id)

            if not other_user.is_activated:
                return wcode.goerror(request,
                                     ["Sorry, user is not defined!", "Page not found: 'user/" + str(id) + "/'"])

            wft = WikiFileSystem()
            wft.load_tree(other_user.file_tree)

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

            # Получаем все последние конспекты пользователя
            publications = Publication.objects.filter(id_author=id, is_public=True)

            context = {
                "user_data": user_data,
                "user_id": get_user_id(request),
                "preview_tree": wft.to_html_preview(only_public=True),
                "publications": reversed(publications),
                "user": other_user,
                "prewiew_publ_text": preview_publ_text,
                "prewiew_publ_title": prewiew_publ_title,
                "prewiew_publ_id": prewiew_publ_id,
                "other_user": True,
            }

            return render(request, 'wiki/user.html', context)

    except User.DoesNotExist:
        return wcode.goerror(request, ["Sorry, user is not defined!", "Page not found: 'user/" + str(id) + "/'"])


# Реальное создание пользователя
def get_create_user(request, key, email):

    # Проверяем на существование такого email и ключа регистрации
    # Осли проверка успешна, пользователя не создаем

    try:
        try_key = key.split("=")[1]
        try_email = email.split("=")[1]
        # Получаем пользователя
        new_user = User.objects.get(email=try_email)
        if new_user.is_activated:
            context = {
                "user_data": check_auth(request),
                "user_id": get_user_id(request),
            }

            return render(request, 'wiki/success_registration.html', context)

        reg_key = RegistrationKey.objects.get(email=try_email, key=try_key)

        # Делаем пользователя активированным
        new_user.is_activated = True
        new_user.save()

        # Удаляем ключ регистрации
        reg_key.delete()

        context = {
            "user_data": check_auth(request),
            "user_id": get_user_id(request),
        }

        return render(request, 'wiki/success_registration.html', context)
    except RegistrationKey.DoesNotExist:
        return HttpResponseRedirect("/")
    except DjangoUser.DoesNotExist:
        return HttpResponseRedirect("/")


# Перед регистрацией пользователя, отправим ему сообщение,
# Сгенерировав в базе данных ключ для регистрации
def get_offer_registration(request, is_invite=None):
    """Регистрация нового пользователя"""

    # Получаем данные формы
    form = request.POST

    # Проверяем на существование такого email.
    # Осли проверка успешна, пользователя не создаем

    simple_user = DjangoUser.objects.filter(email=form["user_email"])
    if not simple_user:
        # Создаем ключ регистрации для нового пользователя
        # Генерируем его случайным образом
        # Плюс, ассоциируем его с email адресом
        gen_chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789"
        result_key = ""
        for i in range(0, 64):
            index_char = random.randrange(0, len(gen_chars))
            result_key += gen_chars[index_char]

        # Получаем текущую дату
        date = str(datetime.datetime.now())
        date = date[:len(date) - 7]

        # Составляем необходимый POST запрос
        post_query = configuration.EMAIL_REGISTRATOR_POST_QUERY_ADDRESS + \
                     "key=" + result_key + "&email=" + form["user_email"]

        # Отправляем его в виде ссылки по почте:
        wcode_manager.send_mail(configuration.EMAIL_REGISTRATOR_SENDER_NAME,
                                configuration.EMAIL_REGISTRATOR_SENDER_PASSWORD,
                                form["user_email"],
                                configuration.EMAIL_REGISTRATOR_SENDER_SUBJECT,
                                configuration.EMAIL_REGISTRATOR_SENDER_TEXT + post_query)

        # Создаем новый ключ регистрации
        new_reg_key = RegistrationKey(key=result_key,
                                      email=form["user_email"],
                                      date=date)
        new_reg_key.save()

        # Создаем нового пользователя
        user = DjangoUser.objects.create_user(username=form["user_email"],
                                              email=form["user_email"],
                                              password=form["user_password"])

        stat = Statistics.objects.get(id_statistics=1)
        # Необходимо для создания id пользователей
        total_reg_users = stat.users_total_reg
        stat.users_total_reg += 1
        stat.users_reg += 1

        # Создаем дерево по умолчанию для юзера
        wft = WikiFileSystem()
        wft.create_tree(total_reg_users)

        # Создаем нового юзера, но делаем его не активным
        new_wiki_user = WikiUser(user=user,
                                 nickname="",
                                 email=form["user_email"],
                                 is_activated=False,
                                 id_user=total_reg_users,
                                 file_tree=wft.get_xml_str(),
                                 preview_publ_id=-1)

        # Если это инвайт регистрация, удаляем ключ и делаем пользователя разработчиком:
        if is_invite:
            is_invite.delete()
            new_developer = Developer(id_developer=total_reg_users,
                                      name_developer=form["user_nickname"])
            new_developer.save()

        # Сохранение всех изменений в БД
        new_wiki_user.save()
        stat.save()

        context = {
            "user_data": check_auth(request),
            "user_id": get_user_id(request),
        }

        return render(request, 'wiki/confirm_registration.html', context)
    else:
        context = {
            "error": "Пользователь с таким Email уже существует",
            "user_data": check_auth(request),
            "user_id": get_user_id(request),
        }
        return render(request, 'wiki/registration.html', context)


def get_create_user_invite(request):
    # Проверяем, на соответствие invite ключа
    try:
        invite_key = InviteKeys.objects.get(key=request.POST.get('invite_key'))

        # Создаем нового пользователя
        return get_offer_registration(request, is_invite=invite_key)
    except InviteKeys.DoesNotExist:
        return wcode.goto('invite_registration')


def get_login_user(request):
    user_email = request.POST.get("user_email", False)
    user_password = request.POST.get("user_password", False)

    try:
        user = authenticate(username=user_email, password=user_password)
        wiki_user = User.objects.get(email=user_email)

        if user is not None and wiki_user.is_activated:
            if user.is_active:
                login(request, user)
                return wcode.goto('index')
            else:
                print(">>>>>>>>>>>>>> WIKI ERROR: disabled account")
                return wcode.goto('index')

        else:
            print(">>>>>>>>>>>>>> WIKI ERROR: invalid login")

        return wcode.goto('index')
    except User.DoesNotExist:
        return wcode.goto('index')


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
