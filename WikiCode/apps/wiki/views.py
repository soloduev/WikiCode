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
from WikiCode.apps.wiki.src.views import group_view
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


# Запрос страницы отдельного конспекта(page.html)
@develop_mode_id
def group(request, id):
    return group_view.get_group(request, id)


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


# Отображение конспекта в режиме презентации
@develop_mode_id
@login_required
def presentation(request, id):
    return publication_view.get_presentation(request, id)


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
def check_password(request):
    return settings_view.get_check_password(request)


@develop_mode
def check_nickname(request):
    return settings_view.get_check_nickname(request)


@develop_mode
def repassword_user(request):
    return settings_view.get_repassword_user(request)


@develop_mode
def renickname_user(request):
    return settings_view.get_renickname_user(request)


@develop_mode
def rename_user(request):
    return settings_view.get_rename_user(request)


@develop_mode
def add_folder_in_tree(request):
    return tree_view.get_add_folder_in_tree(request)


@develop_mode
def del_elem_in_tree(request):
    return tree_view.get_del_elem_in_tree(request)


@develop_mode
def check_folder_for_delete(request):
    return tree_view.get_check_folder_for_delete(request)


@develop_mode
def delete_publ_in_tree(request):
    return tree_view.get_delete_publ_in_tree(request)

@develop_mode_id
def save_main_publ_manager(request, id):
    return publ_manager_view.get_save_main_publ_manager(request, id)\

@develop_mode_id
def save_opt_publ_manager(request, id):
    return publ_manager_view.get_save_opt_publ_manager(request, id)


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


# Добавление динамического комментария к конспекту
@develop_mode_id
@login_required
def reply_dynamic_comment(request, id):
    return publication_view.get_reply_dynamic_comment(request, id)


# Добавление общего комментария к конспекту
@develop_mode_id
@login_required
def add_main_comment(request, id):
    return publication_view.get_add_main_comment(request, id)


# Сохранение изменений в конспекте
@develop_mode_id
@login_required
def save_publication(request, id):
    return publication_view.get_save_publication(request, id)


# Получение абзацев определеноой версии
@develop_mode_id
def get_version(request, id):
    return publication_view.get_get_version(request, id)


# Установление HEAD выбранной версии конспекта
@develop_mode_id
def set_head(request, id):
    return publication_view.get_set_head(request, id)


# Здесь не должно быть никаких декораторов!!!
def login_developer(request):
    return develop_view.get_login_developer(request)


@develop_mode
@login_required
def send_bug(request):
    return error_view.get_send_bug(request)


# Отправка уведомления на заявку на добавления в коллеги
@develop_mode_id
@login_required
def send_request_colleagues(request, id):
    return notifications_view.get_send_request_colleagues(request, id)


# Добавление пользователя в коллеги
@develop_mode_id
@login_required
def add_colleague(request, id):
    return colleagues_view.get_add_colleague(request, id)


# Ajax POST запрос, что уведомление было прочитано
@develop_mode
@login_required
def notification_read(request):
    return notifications_view.get_notification_read(request)


# Удаление пользователя из списка коллег
@develop_mode
@login_required
def delete_colleague(request):
    return colleagues_view.get_delete_colleague(request)


# Удаление уведомления
@develop_mode
@login_required
def delete_notification(request):
    return notifications_view.delete_notification(request)


# Добавление редактора к конспекту
@develop_mode_id
@login_required
def add_white_user(request, id):
    return publ_manager_view.get_add_white_user(request, id)


# Удаление редактора конспекта
@develop_mode_id
@login_required
def del_white_user(request, id):
    return publ_manager_view.get_del_white_user(request, id)


# Добавление пользователя в черный список
@develop_mode_id
@login_required
def add_black_user(request, id):
    return publ_manager_view.get_add_black_user(request, id)


# Удаление пользователя из черного списка
@develop_mode_id
@login_required
def del_black_user(request, id):
    return publ_manager_view.get_del_black_user(request, id)


# Сохранение конспекта в своем дереве конспектов
@develop_mode_id
@login_required
def save_page(request, id):
    return publication_view.get_save_page(request, id)


# Удаление сохраненного конспекта
@develop_mode
@login_required
def remove_saved(request):
    return tree_view.get_remove_saved(request)


# Добавление или удаление звезды конспекту
@develop_mode_id
@login_required
def add_star_publication(request, id):
    return publication_view.get_add_star_publication(request, id)


# Загрузка конспекта в формате markdown
@develop_mode_id
@login_required
def load_md(request, id):
    return publication_view.get_load_md(request, id)


# Получение полного пути к конспекту
@develop_mode
@login_required
def get_path_to_folder(request):
    return publication_view.get_get_path_to_folder(request)


# Получение полного пути к конспекту
@develop_mode_id
@login_required
def get_path_to_folder_id(request, id):
    return publication_view.get_get_path_to_folder(request)


# Получение полного пути к конспекту
@develop_mode_id
@login_required
def comment_rating_up(request, id):
    return publication_view.get_comment_rating_up(request, id)


# Получение полного пути к конспекту
@develop_mode_id
@login_required
def comment_rating_down(request, id):
    return publication_view.get_comment_rating_down(request, id)


# Перемещение конспекта
@develop_mode
@login_required
def move_publication(request):
    return tree_view.get_move_publication(request)





