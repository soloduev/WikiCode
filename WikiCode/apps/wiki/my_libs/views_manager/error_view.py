# -*- coding: utf-8 -*-

from django.shortcuts import render
from WikiCode.apps.wiki.my_libs.views_manager.auth import get_user_id


def get_error_page(request, user_data, errors_arr):
    context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
            "error": errors_arr
        }
    return render(request, 'wiki/error.html', context)