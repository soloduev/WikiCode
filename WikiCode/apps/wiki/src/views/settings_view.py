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
from django.http import HttpResponseRedirect
from django.shortcuts import render

from WikiCode.apps.wiki.models import User, Publication, Viewing, BugReport
from WikiCode.apps.wiki.src.views.error_view import get_error_page
from WikiCode.apps.wiki.src.modules.wiki_tree.wiki_tree import WikiFileTree
from .auth import check_auth, get_user_id


def get_settings(request):

    try:
        id = get_user_id(request)

        # Получаем данные пользователя
        user = User.objects.get(id_user=id)
        prewiew_path_publ = ""

        wft = WikiFileTree()
        wft.load_tree(user.file_tree)

        try:
            preview_publ = Publication.objects.get(id_publication=user.preview_publ_id)
            prewiew_path_publ = preview_publ.tree_path.split(":")[0]
            prewiew_path_publ = prewiew_path_publ[:len(prewiew_path_publ)-5]
        except Publication.DoesNotExist:
            pass

        context = {
            "user_data":check_auth(request),
            "user_id": id,
            "user": user,
            "prewiew_path_publ":prewiew_path_publ,
            "preview_tree": wft.to_html_preview()
        }

        return render(request, 'wiki/settings.html', context)
    except User.DoesNotExist:
        get_error_page(request,["Sorry this user is not found!"])


def get_check_password(request):
    """Ajax представление. Проверка на соответствие password текущего пользователя"""
    if request.method == "GET":
        id = get_user_id(request)
        try:
            cur_user = User.objects.get(id_user=id)
            # Проверяем старый пароль на корректность
            is_correct = cur_user.user.check_password(request.GET['password'])
            # Если старый пароль корректен, оповещаем об этом
            if is_correct:
                return HttpResponse('ok', content_type='text/html')
            else:
                return HttpResponse('no', content_type='text/html')
        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')


def get_check_nickname(request):
    """Ajax представление. Проверка на соответствие nickname текущего пользователя"""
    if request.method == "GET":
        id = get_user_id(request)
        try:
            cur_user = User.objects.get(id_user=id)
            # Проверяем старый никнейм на корректность
            # Если старый никнейм корректен, оповещаем об этом
            if cur_user.nickname == request.GET['nickname']:
                return HttpResponse('ok', content_type='text/html')
            else:
                return HttpResponse('no', content_type='text/html')
        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')


def get_repassword_user(request):
    """Ajax представление. Изменение пароля пользователя."""
    if request.method == "POST":
        id = get_user_id(request)
        try:
            # Получаем данные формы
            form = request.POST
            cur_user = User.objects.get(id_user=id)
            # Проверяем старый пароль на корректность
            is_correct = cur_user.user.check_password(form['user_password'])
            # Если старый пароль корректен, проверяем на равенство новый паролей
            new_password = form['user_new_password']
            new_password_repeat = form['user_password_repeat']
            if new_password == new_password_repeat and is_correct:
                cur_user.user.set_password(new_password)
                cur_user.user.save()
                cur_user.save()
                # TODO: Информировать пользователя о том, чтобы он перезашел на платформу,так как он изменил свой пароль
                return HttpResponseRedirect("/")
            else:
                get_error_page(request, ["Sorry passwords incorrect!"])
        except User.DoesNotExist:
            get_error_page(request, ["User is not found!"])
    else:
        return HttpResponse('no', content_type='text/html')


def get_renickname_user(request):
    """Ajax представление. Изменение никнейма пользователя."""
    if request.method == "POST":
        id = get_user_id(request)
        try:
            # Получаем данные формы
            form = request.POST
            cur_user = User.objects.get(id_user=id)
            # Проверяем старый никнейм на корректность
            # Если старый пароль корректен, проверяем на равенство новый паролей
            if cur_user.nickname == form['user_nickname']:
                new_nickname = form['user_new_nickname']
                new_nickname_repeat = form['user_nickname_repeat']
                if new_nickname == new_nickname_repeat:
                    cur_user.nickname = new_nickname

                    # TODO: Также, при изменении nickname, необходимо везде его поменять в БД.
                    # TODO: Данный участок кода необходимо будет оптимизировать в будущем.
                    # TODO: Желательно будет реализовать отдельный модуль, который будет поддерживать целостность БД

                    # Меняем все публикации, где был указан его никнейм
                    try:
                        publications = Publication.objects.filter(id_author=cur_user.id_user)
                        for publ in publications:
                            publ.nickname_author = new_nickname
                            publ.save()
                    except Publication.DoesNotExist:
                        pass
                    # Меняем все просмотры, где был указан его никнейм
                    try:
                        viewings = Viewing.objects.filter(id_user=cur_user.id_user)
                        for view in viewings:
                            view.nickname = new_nickname
                            view.save()
                    except Viewing.DoesNotExist:
                        pass
                    # Меняем все баг-репорты, где был указан его никнейм
                    try:
                        bug_reports = BugReport.objects.filter(id_author=cur_user.id_user)
                        for bug_report in bug_reports:
                            bug_report.nickname_author = new_nickname
                            bug_report.save()
                    except BugReport.DoesNotExist:
                        pass

                    cur_user.save()

                    # TODO: Информировать пользователя о том, чтобы он перезашел на платформу,так как он изменил свой никнейм
                    return HttpResponseRedirect("/")
                else:
                    get_error_page(request, ["Извините, но введенныя Вами новая пара никнеймов не совпадает!"])
            else:
                get_error_page(request, ["Извините, но Ваш старый пароль не корректен!"])
        except User.DoesNotExist:
            get_error_page(request, ["User is not found!"])
    else:
        return HttpResponse('no', content_type='text/html')
