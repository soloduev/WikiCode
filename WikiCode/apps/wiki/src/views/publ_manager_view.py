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

from WikiCode.apps.wiki.models import Publication, User
from WikiCode.apps.wiki.src.views.auth import check_auth, get_user_id
from WikiCode.apps.wiki.src.views.error_view import get_error_page
from WikiCode.apps.wiki.models import User as WikiUser
from WikiCode.apps.wiki.src.views.publication_view import get_publ_manager


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

                return get_publ_manager(request, id)
            else:
                return get_error_page(request, ["У Вас нет доступа к этому конспекту, чтобы управлять им!",
                                                "Вы не являетесь редактором конспекта page/" + str(id) + "/"])

        except Publication.DoesNotExist:
            return get_error_page(request,
                                  ["This is publication not found!", "Page not found: publ_manager/" + str(id) + "/"])

