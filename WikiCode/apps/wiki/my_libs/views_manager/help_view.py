# -*- coding: utf-8 -*-
from django.shortcuts import render

from .auth import check_auth, get_user_id


def get_help(request):

    context = {
        "user_data" : check_auth(request),
        "user_id": get_user_id(request),

    }

    return render(request, 'wiki/help.html', context)
