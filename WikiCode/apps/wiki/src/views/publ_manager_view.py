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