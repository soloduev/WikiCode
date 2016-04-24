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

from WikiCode.apps.wiki.models import User, Publication
from WikiCode.apps.wiki.my_libs.views_manager.error_view import get_error_page
from .auth import check_auth, get_user_id


def get_settings(request):

    try:
        id = get_user_id(request)

        # Получаем данные пользователя
        user = User.objects.get(id_user=id)
        prewiew_path_publ = ""
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
        }

        return render(request, 'wiki/settings.html', context)
    except User.DoesNotExist:
        get_error_page(request,["Sorry this user is not found!"])
