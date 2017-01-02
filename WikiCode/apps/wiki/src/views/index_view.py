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

from WikiCode.apps.wiki.models import Publication
from WikiCode.apps.wiki.settings import wiki_settings
from .auth import check_auth
from .auth import get_user_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_index(request, notify=None):
    """ Возвращает начальную страницу сайта.
    Может принимать notify(сообщение, которое можно вывести после отображения страницы):
    notify:
        {
            'type': 'error|info',
            'text': 'any text',
        }
    """

    if notify is None:
        notify = {'type': 'msg', 'text': ''}

    # Получаем только публичные конспекты
    all_publications = Publication.objects.filter(is_public=True)

    # Срезаем конспекты, если их больше того количества, которое хотим вывести
    if len(all_publications) > wiki_settings.COUNT_LAST_PUBL_SHOW:
        position = len(all_publications) - wiki_settings.COUNT_LAST_PUBL_SHOW
        all_publications = all_publications[position:]

    # Делаем реверс конспектов
    reverse_publications = []

    for publ in reversed(all_publications):
        reverse_publications.append(publ)

    all_publications = reverse_publications

    paginator = Paginator(all_publications, 10)

    page = request.GET.get('page')

    try:
        publications = paginator.page(page)
    except PageNotAnInteger:
        publications = paginator.page(1)
    except EmptyPage:
        publications = paginator.page(paginator.num_pages)

    context = {
        "all_publications": all_publications,
        "publications": publications,
        "user_data": check_auth(request),
        "user_id": get_user_id(request),
        "notify": notify
    }

    return render(request, 'wiki/index.html', context)
