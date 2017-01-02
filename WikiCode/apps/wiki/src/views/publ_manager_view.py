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
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from WikiCode.apps.wiki.models import Publication, User
from WikiCode.apps.wiki.src.modules.wiki_tree.wiki_tree import WikiFileTree
from WikiCode.apps.wiki.src.modules.wiki_permissions.wiki_permissions import WikiPermissions
from WikiCode.apps.wiki.src.views.auth import check_auth, get_user_id
from WikiCode.apps.wiki.src.views.error_view import get_error_page
from WikiCode.apps.wiki.models import User as WikiUser
from WikiCode.apps.wiki.src.views.publication_view import get_publ_manager


def get_save_access(request, id):
    if request.method == "POST":
        try:
            # Получаем конспект, которым хотим управлять
            publication = Publication.objects.get(id_publication=id)

            # Проверяем, является ли автором этого конспекта тот пользователь
            # Который захотел управлять этим конспектом
            current_id = get_user_id(request)
            if current_id == publication.id_author:

                return get_publ_manager(request, id)
            else:
                return get_error_page(request, ["У Вас нет доступа к этому конспекту, чтобы управлять им!",
                                                "Вы не являетесь редактором конспекта page/" + str(id) + "/"])

        except Publication.DoesNotExist:
            return get_error_page(request,
                                  ["This is publication not found!", "Page not found: publ_manager/" + str(id) + "/"])


def get_save_main_publ_manager(request, id):
    if request.method == "POST":
        try:
            # Получаем конспект, которым хотим управлять
            publication = Publication.objects.get(id_publication=id)

            current_id = get_user_id(request)
            if current_id == publication.id_author:
                # Получаем данные с формы
                new_title = request.POST.get("title_publication")
                new_description = request.POST.get("desription_publication")
                new_path = request.POST.get("path_publication")  # TODO: Необходимо реализовать сохранение нового пути

                if new_title.strip(" \r\n\t") and new_description.strip(" \r\n\t"):
                    publication.title = new_title
                    publication.description = new_description
                    publication.save()
                    return get_publ_manager(request,
                                            id,
                                            notify={'type': 'info',
                                                    'text': 'Заголовок и описание конспекта успешно изменены!\n\n\n'})

                return get_publ_manager(request,
                                        id,
                                        notify={'type': 'error',
                                                'text': 'Заголовок и описание изменить не удалось!\n\n\n'})
            else:
                return get_error_page(request, ["У Вас нет доступа к этому конспекту, чтобы управлять им!",
                                                "Вы не являетесь редактором конспекта page/" + str(id) + "/"])
        except Publication.DoesNotExist:
            return get_error_page(request,
                                  ["This is publication not found!", "Page not found: publ_manager/" + str(id) + "/"])


def get_save_opt_publ_manager(request, id):
    if request.method == "POST":
        try:
            # Получаем конспект, которым хотим управлять
            publication = Publication.objects.get(id_publication=id)

            current_id = get_user_id(request)
            if current_id == publication.id_author:
                publication.is_public = request.POST.get("access-opt", False)
                publication.is_dynamic_paragraphs = request.POST.get("dynamic-opt", False)
                publication.is_general_comments = request.POST.get("main-comments-opt", False)
                publication.is_contents = request.POST.get("contents-opt", False)
                publication.is_protected_edit = request.POST.get("private-edit-opt", False)
                publication.is_files = request.POST.get("files-opt", False)
                publication.is_links = request.POST.get("links-opt", False)
                publication.is_versions = request.POST.get("versions-opt", False)
                publication.is_show_author = request.POST.get("show-author-opt", False)
                publication.is_loading = request.POST.get("loading-opt", False)
                publication.is_saving = request.POST.get("saving-opt", False)
                publication.is_starring = request.POST.get("rating-opt", False)
                publication.is_file_tree = request.POST.get("file-tree-opt", False)

                cur_user = User.objects.get(id_user=current_id)

                wft = WikiFileTree()
                wft.load_tree(cur_user.file_tree)
                wft.reaccess_publication(publication.id_publication, "public" if request.POST.get("access-opt", False) else "private")

                cur_user.file_tree = wft.get_xml_str()

                cur_user.save()
                publication.save()

                return get_publ_manager(request,
                                        id,
                                        notify={'type': 'info',
                                                'text': 'Все настройки конспекта успешно изменены!\n\n\n'})
            else:
                return get_error_page(request, ["У Вас нет доступа к этому конспекту, чтобы управлять им!",
                                                "Вы не являетесь редактором конспекта page/" + str(id) + "/"])
        except Publication.DoesNotExist:
            return get_error_page(request,
                                  ["This is publication not found!", "Page not found: publ_manager/" + str(id) + "/"])

        except User.DoesNotExist:
            return get_error_page(request,
                                  ["User not found!"])


def get_add_white_user(request, id):
    if request.method == "POST":
        try:
            # Получаем конспект, которым хотим управлять
            publication = Publication.objects.get(id_publication=id)

            white_user = request.POST.get("add_white_user")

            try:
                find_user = User.objects.get(nickname=white_user)

                if find_user.id_user == get_user_id(request):
                    return get_publ_manager(request,
                                            id,
                                            notify={'type': 'error',
                                                    'text': 'Вы и так являетесь автором конспекта.\n'
                                                            'Вы не можете назначить себя редактором.\n\n'})

                wp = WikiPermissions()
                wp.load_permissions(publication.permissions)
                white_users = wp.get_white_list()
                is_find = False
                for user in white_users:
                    if str(find_user.id_user) == str(user["id"]):
                        is_find = True

                if not is_find:
                    wp.add_to_white_list(find_user.id_user, find_user.nickname, "editor", "Редактор")
                    publication.permissions = wp.get_xml_str()
                    publication.save()

                    return get_publ_manager(request,
                                        id,
                                        notify={'type': 'info',
                                                'text': 'Назначен новый редактор конспекта.\n\n\n'})
                else:
                    return get_publ_manager(request,
                                        id,
                                        notify={'type': 'error',
                                                'text': 'Данный пользователь уже назначен редактором.\n\n\n'})

            except User.DoesNotExist:
                return get_publ_manager(request,
                                        id,
                                        notify={'type': 'error',
                                                'text': 'Пользователя с таким nickname не существует.\n'
                                                        'Новый редактор не назначен.\n\n'})

        except Publication.DoesNotExist:
            return get_error_page(request,
                                  ["This is publication not found!", "Page not found: publ_manager/" + str(id) + "/"])


def get_del_white_user(request, id):
    if request.method == "POST":
        try:
            # Получаем конспект, которым хотим управлять
            publication = Publication.objects.get(id_publication=id)

            del_user_nickname = request.POST.get("publ_editor")

            if not del_user_nickname:
                return get_publ_manager(request,
                                        id,
                                        notify={'type': 'error',
                                                'text': 'Вы не указали удаляемого пользователя.\n\n\n'})

            try:
                find_user = User.objects.get(nickname=del_user_nickname)

                wp = WikiPermissions()
                wp.load_permissions(publication.permissions)
                white_users = wp.get_white_list()
                is_find = False
                for user in white_users:
                    if str(find_user.id_user) == str(user["id"]):
                        is_find = True

                if is_find:
                    wp.remove_from_white_list(find_user.id_user)
                    publication.permissions = wp.get_xml_str()
                    publication.save()

                    return get_publ_manager(request,
                                            id,
                                            notify={'type': 'info',
                                                    'text': 'Пользователь успешно удален из списка редакторов.\n\n\n'})
                else:
                    return get_publ_manager(request,
                                            id,
                                            notify={'type': 'error',
                                                    'text': 'Пользователь уже удален из списка редакторов\n\n\n'})
            except User.DoesNotExist:
                return get_publ_manager(request,
                                        id,
                                        notify={'type': 'error',
                                                'text': 'Удаляемого пользователя не существует.\n\n\n'})

        except Publication.DoesNotExist:
            return get_error_page(request,
                                  ["This is publication not found!", "Page not found: publ_manager/" + str(id) + "/"])


def get_add_black_user(request, id):
    if request.method == "POST":
        try:
            # Получаем конспект, которым хотим управлять
            publication = Publication.objects.get(id_publication=id)

        except Publication.DoesNotExist:
            return get_error_page(request,
                                  ["This is publication not found!", "Page not found: publ_manager/" + str(id) + "/"])


def get_del_black_user(request, id):
    if request.method == "POST":
        try:
            # Получаем конспект, которым хотим управлять
            publication = Publication.objects.get(id_publication=id)

        except Publication.DoesNotExist:
            return get_error_page(request,
                                  ["This is publication not found!", "Page not found: publ_manager/" + str(id) + "/"])