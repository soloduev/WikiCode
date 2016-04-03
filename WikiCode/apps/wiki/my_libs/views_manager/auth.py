# -*- coding: utf-8 -*-


def check_auth(request):
    """Проверка аутентифицирован ли пользователь"""
    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    return user_data