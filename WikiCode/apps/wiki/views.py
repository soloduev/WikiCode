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


from WikiCode.apps.wiki.my_libs.views_manager import index_view
from WikiCode.apps.wiki.my_libs.views_manager import about_view
from WikiCode.apps.wiki.my_libs.views_manager import publication_view
from WikiCode.apps.wiki.my_libs.views_manager import settings_view
from WikiCode.apps.wiki.my_libs.views_manager import user_view
from WikiCode.apps.wiki.my_libs.views_manager import registration_view
from WikiCode.apps.wiki.my_libs.views_manager import tree_view
from django.contrib.auth.decorators import login_required


def index(request):
    return index_view.get_index(request)


def about(request):
    return about_view.get_about(request)


@login_required
def create(request):
    return publication_view.get_create(request)


def page(request, id):
    return publication_view.get_page(request, id)


@login_required
def settings(request):
    return settings_view.get_settings(request)


@login_required
def user(request, id):
    return user_view.get_user(request, id)


def registration(request):
    return registration_view.get_registration(request)


def create_user(request):
    return user_view.get_create_user(request)


def login_user(request):
    return user_view.get_login_user(request)


@login_required
def logout_user(request):
    return user_view.get_logout_user(request)


@login_required
def create_page(request):
    return publication_view.get_create_page(request)


@login_required
def tree_manager(request):
    return tree_view.get_tree_manager(request)


@login_required
def publ_manager(request, id):
    return publication_view.get_publ_manager(request, id)


def check_nickname(request):
    return registration_view.get_check_nickname(request)


def check_email(request):
    return registration_view.get_check_email(request)


def add_folder_in_tree(request):
    return tree_view.get_add_folder_in_tree(request)


def del_elem_in_tree(request):
    return tree_view.get_del_elem_in_tree(request)


def check_folder_for_delete(request):
    return tree_view.get_check_folder_for_delete(request)


def delete_publ_in_tree(request):
    return tree_view.get_delete_publ_in_tree(request)


def rename_publ_in_tree(request):
    return tree_view.get_rename_publ_in_tree(request)


def rename_folder_in_tree(request):
    return tree_view.get_rename_folder_in_tree(request)


def add_comment_in_wiki_page(request, id):
    return publication_view.get_add_comment_in_wiki_page(request, id)