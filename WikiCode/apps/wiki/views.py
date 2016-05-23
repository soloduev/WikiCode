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


@develop_mode
def index(request):
    return index_view.get_index(request)


@develop_mode
def about(request):
    return about_view.get_about(request)


@develop_mode
@login_required
def create(request):
    return publication_view.get_create(request)


@develop_mode_id
def page(request, id):
    return publication_view.get_page(request, id)


@develop_mode
@login_required
def settings(request):
    return settings_view.get_settings(request)


@develop_mode_id
@login_required
def user(request, id):
    return user_view.get_user(request, id)


@develop_mode
def registration(request):
    return registration_view.get_registration(request)


def login(request):
    return user_view.get_login(request)


@develop_mode
def create_user(request):
    return user_view.get_create_user(request)


@develop_mode
def login_user(request):
    return user_view.get_login_user(request)


@develop_mode
@login_required
def logout_user(request):
    return user_view.get_logout_user(request)


@develop_mode
@login_required
def create_page(request):
    return publication_view.get_create_page(request)


@develop_mode
@login_required
def tree_manager(request):
    return tree_view.get_tree_manager(request)


@develop_mode_id
@login_required
def publ_manager(request, id):
    return publication_view.get_publ_manager(request, id)


@develop_mode
@login_required
def colleagues(request):
    return colleagues_view.get_colleagues(request)


@develop_mode
@login_required
def add_colleague(request):
    return colleagues_view.get_add_colleague(request)


@develop_mode
@login_required
def send_request_for_colleagues(request):
    return notifications_view.get_send_request_for_colleagues(request)


@develop_mode
@login_required
def read_notification(request):
    return notifications_view.get_read_notification(request)


@develop_mode
@login_required
def remove_notification(request):
    return notifications_view.get_remove_notification(request)


@develop_mode
@login_required
def send_answer_message(request):
    return notifications_view.get_send_answer_message(request)


@develop_mode
@login_required
def remove_colleague(request):
    return colleagues_view.get_remove_colleague(request)


@develop_mode
@login_required
def colleague_send_message(request):
    return notifications_view.get_colleague_send_message(request)


@develop_mode
@login_required
def notifications(request):
    return notifications_view.get_notifications(request)


@develop_mode
@login_required
def bug_report(request):
    return error_view.get_bug_report(request)


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
def add_folder_in_saved_tree(request):
    return tree_view.get_add_folder_in_saved_tree(request)


@develop_mode
def del_elem_in_tree(request):
    return tree_view.get_del_elem_in_tree(request)


@develop_mode
def del_elem_in_tree_saved(request):
    return tree_view.get_del_elem_in_tree_saved(request)


@develop_mode
def del_publ_in_tree_saved(request):
    return tree_view.get_del_publ_in_tree_saved(request)


@develop_mode
def check_folder_for_delete(request):
    return tree_view.get_check_folder_for_delete(request)


@develop_mode
def check_folder_for_delete_saved(request):
    return tree_view.get_check_folder_for_delete_saved(request)


@develop_mode
def delete_publ_in_tree(request):
    return tree_view.get_delete_publ_in_tree(request)


@develop_mode_id
def save_access(request, id):
    return publ_manager_view.get_save_access(request, id)


@develop_mode
def rename_publ_in_tree(request):
    return tree_view.get_rename_publ_in_tree(request)


@develop_mode
def rename_folder_in_tree(request):
    return tree_view.get_rename_folder_in_tree(request)


@develop_mode
def set_preview_publ_in_tree(request):
    return tree_view.get_set_preview_publ_in_tree(request)


@develop_mode_id
@login_required
def add_comment_in_wiki_page(request, id):
    return publication_view.get_add_comment_in_wiki_page(request, id)


@develop_mode_id
@login_required
def add_dynamic_comment_in_wiki_page(request, id):
    return publication_view.get_add_dynamic_comment_in_wiki_page(request, id)


@develop_mode_id
@login_required
def like_wiki_page(request, id):
    return publication_view.get_like_wiki_page(request, id)


@develop_mode_id
@login_required
def import_wiki_page(request, id):
    return publication_view.get_import_wiki_page(request, id)


@develop_mode_id
@login_required
def send_answer_comment(request, id):
    return notifications_view.get_send_answer_comment(request, id)


@develop_mode_id
@login_required
def like_user(request, id):
    return user_view.get_like_user(request, id)


@develop_mode_id
@login_required
def user_send_message(request, id):
    return notifications_view.get_user_send_message(request, id)


@develop_mode_id
@login_required
def user_send_request_for_colleagues(request, id):
    return notifications_view.get_send_request_for_colleagues(request)


@develop_mode
@login_required
def check_nickname_for_add_editor(request):
    return publ_manager_view.get_check_nickname_for_add_editor(request)


@develop_mode
@login_required
def add_editor(request):
    return publ_manager_view.get_add_editor(request)


@develop_mode
@login_required
def remove_editor(request):
    return publ_manager_view.get_remove_editor(request)


# Здесь не должно быть никаких декораторов!!!
def login_developer(request):
    return develop_view.get_login_developer(request)


@develop_mode
@login_required
def send_bug(request):
    return error_view.get_send_bug(request)
