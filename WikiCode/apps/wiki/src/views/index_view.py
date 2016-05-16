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
from .auth import check_auth
from .auth import get_user_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_index(request):

    all_publications = Publication.objects.filter(is_public=True)
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
            "publications":publications,
            "user_data": check_auth(request),
            "user_id": get_user_id(request),
    }

    return render(request, 'wiki/index.html', context)
