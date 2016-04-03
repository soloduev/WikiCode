# -*- coding: utf-8 -*-
from django.shortcuts import render

from WikiCode.apps.wiki.models import Publication
from .auth import check_auth


def get_index(request):

    all_publications = Publication.objects.all()

    context = {
            "all_publications": all_publications,
            "user_data": check_auth(request)
    }

    return render(request, 'wiki/index.html', context)
