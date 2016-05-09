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
from django.contrib.auth import authenticate, login
from django.shortcuts import render

from WikiCode.apps.wiki.models import Publication, Developer
from WikiCode.apps.wiki.src.views.auth import check_auth, get_user_id


def get_login_developer(request):
    user_name = request.POST['developer_name']
    user_password = request.POST['developer_password']

    try:
        developer = Developer.objects.get(name_developer=user_name)
        user = authenticate(username=user_name, password=user_password)

        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                print(">>>>>>>>>>>>>> WIKI ERROR: disabled account")
                user_id = get_user_id(request)
                user_data = check_auth(request)

                context = {
                    "user_data": user_data,
                    "user_id": user_id,
                }
                return render(request, 'wiki/develop_mode.html', context)


        else:
            print(">>>>>>>>>>>>>> WIKI ERROR: invalid login")
            user_id = get_user_id(request)
            user_data = check_auth(request)

            context = {
                "user_data": user_data,
                "user_id": user_id,
            }
            return render(request, 'wiki/develop_mode.html', context)

        all_publications = Publication.objects.filter(is_public=True)

        context = {
            "all_publications": all_publications,
            "user_data": check_auth(request),
            "user_id": get_user_id(request),
        }

        return render(request, 'wiki/index.html', context)
    except Developer.DoesNotExist:
        user_id = get_user_id(request)
        user_data = check_auth(request)

        context = {
            "user_data": user_data,
            "user_id": user_id,
        }
        return render(request, 'wiki/develop_mode.html', context)

