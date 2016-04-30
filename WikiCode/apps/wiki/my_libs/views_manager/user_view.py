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
from django.views.decorators.csrf import csrf_protect

from .auth import check_auth, get_user_id
from django.shortcuts import render
from WikiCode.apps.wiki.models import User as WikiUser, Like
from django.contrib.auth.models import User as DjangoUser
from WikiCode.apps.wiki.models import Statistics
from WikiCode.apps.wiki.models import Publication
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from WikiCode.apps.wiki.my_libs.trees_management.manager import WikiTree
from WikiCode.apps.wiki.models import User
from WikiCode.apps.wiki.my_libs.views_manager.error_view import get_error_page
import datetime

def get_user(request, id):

    user_data = check_auth(request)
    try:
        user = User.objects.get(email=user_data)
        if str(get_user_id(request)) == id:
            wt = WikiTree(user.id_user)
            wt.load_tree(user.tree)
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
                    "preview_tree": wt.generate_html_preview(),
                    "user":user,
                    "prewiew_publ_text":preview_publ_text,
                    "prewiew_publ_title":prewiew_publ_title,
                    "prewiew_publ_id":prewiew_publ_id,
                }

                return render(request, 'wiki/user.html', context)
            else:
                return get_error_page(request, ["Sorry, id user problem!", "Page not found: 'user/" + str(id) + "/'"])
        else:
            other_user = User.objects.get(id_user=id)
            wt = WikiTree(other_user.id_user)
            wt.load_tree(other_user.tree)

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
                "preview_tree": wt.generate_html_preview(),
                "user":other_user,
                "prewiew_publ_text": preview_publ_text,
                "prewiew_publ_title": prewiew_publ_title,
                "prewiew_publ_id": prewiew_publ_id,
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
            new_tree = WikiTree(total_reg_users)

            # Создаем нового юзера
            new_wiki_user = WikiUser(user=user,
                                     nickname=form["user_nickname"],
                                     email=form["user_email"],
                                     id_user=total_reg_users,
                                     tree=new_tree.get_tree(),
                                     avatar="none.jpg",
                                     name="anonymous",
                                     likes=0,
                                     publications=0,
                                     imports=0,
                                     comments=0,
                                     imports_it=0,
                                     commented_it=0,
                                     preview_publ_id=-1)



            user = authenticate(username=form["user_nickname"], password=form["user_password"])

            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    print(">>>>>>>>>>>>>> WIKI ERROR: disabled account")

            else:
                print(">>>>>>>>>>>>>> WIKI ERROR: invalid login")


            all_publications = Publication.objects.filter(is_public=True)

            # Сохранение всех изменений в БД
            new_wiki_user.save()
            stat.save()

            context = {
                "all_publications": all_publications,
                "user_data": check_auth(request),
                "user_id": get_user_id(request),
            }
            return render(request, 'wiki/index.html', context)
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
        else:
            print(">>>>>>>>>>>>>> WIKI ERROR: disabled account")

    else:
        print(">>>>>>>>>>>>>> WIKI ERROR: invalid login")


    all_publications = Publication.objects.filter(is_public=True)

    context = {
        "all_publications": all_publications,
        "user_data": check_auth(request),
        "user_id": get_user_id(request),
    }

    return render(request, 'wiki/index.html', context)


def get_logout_user(request):

    logout(request)
    all_publications = Publication.objects.filter(is_public=True)

    context = {
        "all_publications": all_publications,
        "user_data": check_auth(request),
        "user_id": get_user_id(request),
    }

    return render(request, 'wiki/index.html', context)


@csrf_protect
def get_like_user(request, id):
    """Ajax представление. Like определенному пользователю."""
    if request.method == "POST":
        try:
            # Получаем пользователя захотевшего поставить лайк
            id_user = int(get_user_id(request))

            if id_user == -1:
                return HttpResponse('no', content_type='text/html')
            else:
                # Получаем текущую дату
                date = str(datetime.datetime.now())
                date = date[:len(date) - 7]

                # Получаем User
                user_set = User.objects.get(id_user=id_user)
                # Получаем пользователя на которого поставлен лайк
                user_get = User.objects.get(id_user=id)

                # Проверяем, не стоит ли like уже у этого пользователя на этого пользователя
                try:
                    like = Like.objects.get(id_user=id_user, id_user_like=id)
                    # Лайк стоит, убираем
                    like.delete()
                    user_get.likes -= 1
                    user_get.save()
                except Like.DoesNotExist:
                    # Лайк не стоит. Ставим
                    new_like = Like(id_user=id_user,
                                    nickname=user_set.nickname,
                                    type="user",
                                    id_publ_like=-1,
                                    id_user_like=id,
                                    date=date)
                    new_like.save()
                    user_get.likes += 1
                    user_get.save()

                return HttpResponse('ok', content_type='text/html')
        except User.DoesNotExist:
            return get_error_page(request, ["This is user is not found!"])
    else:
        return HttpResponse('no', content_type='text/html')
