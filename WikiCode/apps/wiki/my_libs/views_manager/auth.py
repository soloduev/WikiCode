# -*- coding: utf-8 -*-

from WikiCode.apps.wiki.models import User

def check_auth(request):
    """Проверка аутентифицирован ли пользователь"""
    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    return user_data


def get_user_id(request):
    user_data = check_auth(request)
    id_user = 0;
    if user_data != "None":
        user = User.objects.get(email=user_data)
        id_user = user.id_user
    return id_user