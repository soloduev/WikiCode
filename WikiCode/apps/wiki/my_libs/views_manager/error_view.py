# -*- coding: utf-8 -*-

from django.shortcuts import render
from WikiCode.apps.wiki.my_libs.views_manager.auth import get_user_id, check_auth


def get_error_page(request, errors_arr):
    context = {
            "user_data": check_auth(request),
            "user_id": get_user_id(request),
            "error": errors_arr
        }
    return render(request, 'wiki/error.html', context)