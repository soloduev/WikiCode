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

from WikiCode.apps.wiki.models import Publication, Editor, User
from WikiCode.apps.wiki.my_libs.views_manager.auth import check_auth, get_user_id
from WikiCode.apps.wiki.my_libs.views_manager.error_view import get_error_page
from WikiCode.apps.wiki.models import User as WikiUser
from WikiCode.apps.wiki.my_libs.views_manager.publication_view import get_publ_manager


def get_save_access(request, id):
    if request.method == "POST":
        try:
            # Получаем пользователя
            user_data = check_auth(request)

            # Получаем конспект, которым хотим управлять
            publication = Publication.objects.get(id_publication=id)

            # Проверяем, является ли автором этого конспекта тот пользователь
            # Который захотел управлять этим конспектом
            current_id = get_user_id(request)
            if current_id == publication.id_author:

                # Теперь получаем изменения и применяем их
                form = request.POST
                level_access = form["level_access"]
                if level_access == "Публичный":
                    publication.is_public = True
                    publication.is_private = False
                    publication.save()
                elif level_access == "Приватный":
                    # Если до этого конспект был публичным
                    # Очищаем всех редакторов этого конспекта
                    if publication.is_public:
                        try:
                            editors = Editor.objects.filter(publication=publication)
                            for editor in editors:
                                editor.delete()
                        except Editor.DoesNotExist:
                            pass

                    publication.is_public = False
                    publication.is_private = True
                    publication.save()



                return get_publ_manager(request, id)
            else:
                return get_error_page(request, ["У Вас нет доступа к этому конспекту, чтобы управлять им!",
                                                "Вы не являетесь редактором конспекта page/" + str(id) + "/"])

        except Publication.DoesNotExist:
            return get_error_page(request,
                                  ["This is publication not found!", "Page not found: publ_manager/" + str(id) + "/"])



def get_check_nickname_for_add_editor(request):
    """Ajax запрос на проверку возможности назначения пользователя в редакторы"""

    if request.method == "GET":
        request.session['nickname'] = request.GET['nickname']
        nickname = request.GET['nickname']
        id_publ_for_add_editor = request.GET["id_publ_for_add_editor"]

        try:
            user = WikiUser.objects.get(nickname=nickname)

            # Проверяем, не является ли этот пользователь автором данного конспекта
            try:
                publication = Publication.objects.get(id_publication=id_publ_for_add_editor)

                if publication.nickname_author == nickname:
                    return HttpResponse('author', content_type='text/html')
                else:
                    editors = Editor.objects.filter(publication=publication)
                    for editor in editors:
                        if editor.nickname_user == nickname:
                            return HttpResponse('repeat', content_type='text/html')
                    return HttpResponse('ok', content_type='text/html')

            except Publication.DoesNotExist:
                return HttpResponse('no', content_type='text/html')
            except User.DoesNotExist:
                return HttpResponse('no', content_type='text/html')
            except Editor.DoesNotExist:
                return HttpResponse('no', content_type='text/html')
        except WikiUser.DoesNotExist:
            return HttpResponse('no', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_add_editor(request):
    """Ajax запрос на добавления пользователя в редакторы"""
    if request.method == "POST":
        request.session['nickname'] = request.POST['nickname']
        _nickname = request.POST['nickname']
        id_publ = request.POST['id_publ_for_add_editor']

        try:
            user = WikiUser.objects.get(nickname=_nickname)
            # Добавляем пользователя в редакторы
            try:
                # Получаем конспект, к которому назначаем нового редактора
                publication = Publication.objects.get(id_publication=id_publ)
                # Получаем пользователя которого необходимо назначить редактором
                user = User.objects.get(nickname=_nickname)

                new_editor = Editor(publication=publication,
                                    id_user=user.id_user,
                                    nickname_user=user.nickname,
                                    status="editor")
                new_editor.save()
                return HttpResponse('ok', content_type='text/html')

            except Publication.DoesNotExist:
                return HttpResponse('no', content_type='text/html')
            except User.DoesNotExist:
                return HttpResponse('no', content_type='text/html')

        except WikiUser.DoesNotExist:
            return HttpResponse('no', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')