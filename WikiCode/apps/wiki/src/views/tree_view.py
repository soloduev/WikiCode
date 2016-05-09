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


import os

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from WikiCode.apps.wiki.settings import wiki_settings
from .auth import check_auth, get_user_id
from WikiCode.apps.wiki.models import User, Publication, Statistics
from WikiCode.apps.wiki.src.trees_management.manager import WikiTree


def get_tree_manager(request):
    user_data = check_auth(request)
    try:
        user = User.objects.get(email=user_data)
        wt = WikiTree(user.id_user)
        wt.load_tree(user.tree)

        context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
            "preview_tree": wt.generate_html_preview(),
            "dynamic_tree": wt.generate_html_dynamic(),
        }

        return render(request, 'wiki/tree_manager.html', context)
    except User.DoesNotExist:
        context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
        }
        return render(request, 'wiki/tree_manager.html', context)


@csrf_protect
def get_add_folder_in_tree(request):
    """Ajax представление. Добавление папки в дерево пользователя"""

    if request.method == "POST":
        answer = request.POST.get('answer')
        user_data = check_auth(request)
        split_answer = answer.split("^^^")
        folder_name = split_answer[0]
        path = split_answer[1].split(":")[0]

        try:
            user = User.objects.get(email=user_data)
            wt = WikiTree(user.id_user)
            wt.load_tree(user.tree)
            wt.add_folder(path, folder_name)
            user.tree = wt.get_tree()
            user.save()

            return HttpResponse('ok', content_type='text/html')

        except User.DoesNotExist:
            context = {
                "user_data": user_data,
                "user_id": get_user_id(request),
            }
            return render(request, 'wiki/tree_manager.html', context)

    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_del_elem_in_tree(request):
    """Ajax представление. Удаление элемента в дереве пользователя"""

    if request.method == "POST":
        path_publ = request.POST.get('answer')
        user_data = check_auth(request)

        if path_publ.split(":")[0] == "Personal/" or path_publ.split(":")[0] == "Imports/":
            return HttpResponse('no', content_type='text/html')

        try:
            user = User.objects.get(email=user_data)
            wt = WikiTree(user.id_user)
            wt.load_tree(user.tree)

            if wt.check_folder_for_delete(path_publ.split(":")[0]):
                wt.delete_folder(path_publ.split(":")[0])
                user.tree = wt.get_tree()
                user.save()
                return HttpResponse('ok', content_type='text/html')
            else:
                return HttpResponse('no', content_type='text/html')

        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_check_folder_for_delete(request):
    """Ajax представление. Проверка папку на пустоту, для ее удаления"""

    if request.method == "POST":
        path_publ = request.POST.get('answer')
        user_data = check_auth(request)

        if path_publ.split(":")[0] == "Personal/" or path_publ.split(":")[0] == "Imports/":
            return HttpResponse('no', content_type='text/html')

        try:
            user = User.objects.get(email=user_data)
            wt = WikiTree(user.id_user)
            wt.load_tree(user.tree)

            if wt.check_folder_for_delete(path_publ.split(":")[0]):
                return HttpResponse('ok', content_type='text/html')
            else:
                return HttpResponse('no', content_type='text/html')

        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_delete_publ_in_tree(request):
    """Ajax представление. Удаление конспекта."""

    if request.method == "POST":
        path_publ = request.POST.get('answer')
        user_data = check_auth(request)
        arr = path_publ.split(":")
        id_publ = arr[1]

        try:
            # Получаем удаляемую публикацию
            publication = Publication.objects.get(id_publication=id_publ)
            # Получаем автора этой публикации
            user = User.objects.get(email=user_data)
            # Получаем статистику сайта
            stat = Statistics.objects.get(id_statistics=1)

            # Начинаем производить достаточно громоздкое удаление

            # Получаем дерево пользователя

            # Устанавливаем id пользователя
            wt = WikiTree(user.id_user)
            # Загружаем его дерево
            wt.load_tree(user.tree)
            # Удаляем публикацию по указанному пути
            wt.delete_publication(arr[0])
            user.tree = wt.get_tree()

            # Уменьшаем количество публикаций у пользователя
            user.publications -= 1
            # Уменьшаем количество публикаций в глобальной статистике
            stat.publications_delete += 1

            # Удаляем html файл этой публикации
            os.remove(wiki_settings.DELETE_PUBLICATION_PATH + str(id_publ) + ".html")

            publication.delete()
            user.save()
            stat.save()

            return HttpResponse('ok', content_type='text/html')

        except Publication.DoesNotExist:
            return HttpResponse('no', content_type='text/html')
        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')
        except Statistics.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_rename_publ_in_tree(request):
    """Ajax представление. Переименование конспекта конспекта."""

    if request.method == "POST":
        answer = request.POST.get('answer')
        user_data = check_auth(request)
        arr = str(answer).split("^^^")
        new_name_publ = arr[0]
        path = arr[1].split(":")[0]
        id = arr[1].split(":")[1]

        try:
            user = User.objects.get(email=user_data)
            publication = Publication.objects.get(id_publication=id)
            wt = WikiTree(user.id_user)
            wt.load_tree(user.tree)
            is_rename = wt.rename_publication(path, new_name_publ)
            # Пока переименование конспекта осуществиться даже, если конспект с таким именем уже существует
            if is_rename:
                publication.title = new_name_publ
                user.tree = wt.get_tree()
                # Теперь переименовываем заголовок конспекта внутри его html содержания
                with open("WikiCode/apps/wiki/generate_pages/gen_page.gen", "r", encoding='utf-8') as f:
                    gen_page = f.read()
                first_part = "<!DOCTYPE html><html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"><title>" + \
                             new_name_publ + '</title></head><xmp theme="' + publication.theme.lower() + '" style="display:none;">'
                second_part = publication.text
                ready_page = first_part + second_part + gen_page
                f = open("media/publications/" + id + ".html", 'tw', encoding='utf-8')
                f.close()

                with open("media/publications/" + id + ".html", "wb") as f:
                    f.write(ready_page.encode("utf-8"))
                publication.save()
                user.save()

            return HttpResponse('ok', content_type='text/html')
        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')
        except Publication.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_rename_folder_in_tree(request):
    """Ajax представление. Переименование папки"""
    if request.method == "POST":
        # Важно понимать, что при переименовывании папки, все конспекты внутри него, МЕНЯЮТ СВОЙ ПУТЬ В ДЕРЕВЕ!!!

        return HttpResponse('no', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_set_preview_publ_in_tree(request):
    """Ajax представление. Установление preview конспекта"""

    if request.method == "POST":
        publ = request.POST.get('publ')
        user_id = get_user_id(request)

        # Получаем id той публикации, которую хотим сделать превью
        id_publ = int(publ.split(":")[1])

        try:
            user = User.objects.get(id_user=user_id)
            user.preview_publ_id = id_publ
            user.save()
            return HttpResponse('ok', content_type='text/html')
        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')
