# -*- coding: utf-8 -*-
from django.shortcuts import render

from .auth import check_auth


def get_about(request):

    context = {
        "user_data" : check_auth(request),
    }

    return render(request, 'wiki/about.html', context)
