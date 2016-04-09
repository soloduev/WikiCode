# -*- coding: utf-8 -*-
from WikiCode.apps.wiki.my_libs.views_manager import index_view
from WikiCode.apps.wiki.my_libs.views_manager import about_view
from WikiCode.apps.wiki.my_libs.views_manager import publication_view
from WikiCode.apps.wiki.my_libs.views_manager import help_view
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


@login_required
def edit(request):
    return publication_view.get_edit(request)


def help(request):
    return help_view.get_help(request)


def page(request, id):
    return publication_view.get_page(request, id)


@login_required
def settings(request):
    return settings_view.get_settings(request)


@login_required
def user(request):
    return user_view.get_user(request)


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


def check_nickname(request):
    return registration_view.get_check_nickname(request)


def check_email(request):
    return registration_view.get_check_email(request)

def add_folder_in_tree(request):
    return tree_view.get_add_folder_in_tree(request)

def del_elem_in_tree(request):
    return tree_view.get_del_elem_in_tree(request)