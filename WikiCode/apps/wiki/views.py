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


from WikiCode.apps.wiki.src.views import index_view
from WikiCode.apps.wiki.src.views import about_view
from WikiCode.apps.wiki.src.views import publication_view
from WikiCode.apps.wiki.src.views import settings_view
from WikiCode.apps.wiki.src.views import user_view
from WikiCode.apps.wiki.src.views import registration_view
from WikiCode.apps.wiki.src.views import tree_view
from WikiCode.apps.wiki.src.views import publ_manager_view
from WikiCode.apps.wiki.src.views import develop_view
from WikiCode.apps.wiki.src.views import error_view
from WikiCode.apps.wiki.src.views import colleagues_view
from WikiCode.apps.wiki.src.views import notifications_view
from django.contrib.auth.decorators import login_required
from WikiCode.apps.wiki.src.develop_mode.develop_mode import develop_mode, develop_mode_id


# Запрос главной страницы(index.html)
@develop_mode
def index(request):
    return index_view.get_index(request)


# Запрос информации о платформе(about.html)
@develop_mode
def about(request):
    return about_view.get_about(request)


# Запрос страницы создания конспекта(create.html)
@develop_mode
@login_required
def create(request):
    return publication_view.get_create(request)


# Запрос страницы отдельного конспекта(page.html)
@develop_mode_id
def page(request, id):
    return publication_view.get_page(request, id)


# Запрос страницы настроек зарегестрированного пользователя(settings.html)
@develop_mode
@login_required
def settings(request):
    return settings_view.get_settings(request)


# Запрос страницы любого пользователя(user.html)
@develop_mode_id
@login_required
def user(request, id):
    return user_view.get_user(request, id)


# Запрос страницы регистрации нового пользователя(registration.html)
@develop_mode
def registration(request):
    return registration_view.get_registration(request)


# Запрос страницы авторизации пользователя(login.html)
def login(request):
    return user_view.get_login(request)


# Непосредственное создание нового пользователя
@develop_mode
def create_user(request):
    return user_view.get_create_user(request)


# Непосредственная авторизация пользователя
@develop_mode
def login_user(request):
    return user_view.get_login_user(request)


# Выход пользователя из системы
@develop_mode
@login_required
def logout_user(request):
    return user_view.get_logout_user(request)


# Создание нового конспекта
@develop_mode
@login_required
def create_page(request):
    return publication_view.get_create_page(request)


# Запрос страницы управления деревом конспектов(tree_manager.html)
@develop_mode
@login_required
def tree_manager(request):
    return tree_view.get_tree_manager(request)


# Запрос страницы управления конспектом(publ_manager.html)
@develop_mode_id
@login_required
def publ_manager(request, id):
    return publication_view.get_publ_manager(request, id)


# Запрос страницы коллег пользователя(colleagues.html)
@develop_mode
@login_required
def colleagues(request):
    return colleagues_view.get_colleagues(request)


# Запрос страницы уведомлений пользователя(notifications.html)
@develop_mode
@login_required
def notifications(request):
    return notifications_view.get_notifications(request)


# Запрос страницы баг-репорта(bug_report.html)
@develop_mode
@login_required
def bug_report(request):
    return error_view.get_bug_report(request)


# Ajax запрос на проверку существования никнеймa
@develop_mode
def check_nickname(request):
    return registration_view.get_check_nickname(request)


@develop_mode
def check_email(request):
    return registration_view.get_check_email(request)


@develop_mode
def add_folder_in_tree(request):
    return tree_view.get_add_folder_in_tree(request)


@develop_mode
def del_elem_in_tree(request):
    return tree_view.get_del_elem_in_tree(request)


@develop_mode
def del_publ_in_tree_saved(request):
    return tree_view.get_del_publ_in_tree_saved(request)


@develop_mode
def check_folder_for_delete(request):
    return tree_view.get_check_folder_for_delete(request)


@develop_mode
def delete_publ_in_tree(request):
    return tree_view.get_delete_publ_in_tree(request)



@develop_mode
def rename_publ_in_tree(request):
    return tree_view.get_rename_publ_in_tree(request)


@develop_mode
def rename_folder_in_tree(request):
    return tree_view.get_rename_folder_in_tree(request)


@develop_mode
def set_preview_publ_in_tree(request):
    return tree_view.get_set_preview_publ_in_tree(request)


# Добавление динамического комментария к конспекту
@develop_mode_id
@login_required
def add_dynamic_comment(request, id):
    return publication_view.get_add_dynamic_comment(request, id)


# Здесь не должно быть никаких декораторов!!!
def login_developer(request):
    return develop_view.get_login_developer(request)


@develop_mode
@login_required
def send_bug(request):
    return error_view.get_send_bug(request)
