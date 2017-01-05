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

import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from WikiCode.apps.wiki.models import User, Publication, Statistics, Folder
from WikiCode.apps.wiki.src.modules.wiki_tree.wiki_tree import WikiFileTree
from WikiCode.apps.wiki.src.views.error_view import get_error_page
from .auth import check_auth, get_user_id


def get_tree_manager(request, notify=None):
    """ Возвращает страницу управления файловым деревом пользователя.
        Может принимать notify(сообщение, которое можно вывести после отображения страницы):
        notify:
            {
                'type': 'error|info',
                'text': 'any text',
            }
        """

    if notify is None:
        notify = {'type': 'msg', 'text': ''}

    user_data = check_auth(request)
    try:
        user = User.objects.get(email=user_data)

        wft = WikiFileTree()
        wft.load_tree(user.file_tree)

        context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
            "preview_tree": wft.to_html_preview(),
            "dynamic_tree": wft.to_html_dynamic(),
            "dynamic_tree_folders": wft.to_html_dynamic_folders(),
            "notify": notify,
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
        id_folder = int(split_answer[1])

        try:
            user = User.objects.get(email=user_data)

            # Получаем текущую статистику платформы
            stat = Statistics.objects.get(id_statistics=1)

            wft = WikiFileTree()
            wft.load_tree(user.file_tree)
            wft.create_folder(id=stat.total_folders + 1,
                              name=folder_name,
                              access="public",
                              type="personal",
                              style="blue",
                              view="closed",
                              id_folder=id_folder)

            user.file_tree = wft.get_xml_str()

            # Получаем текущую дату
            date = str(datetime.datetime.now())
            date = date[:len(date) - 7]

            # Создаем новую папку в БД
            new_folder = Folder(id_folder=stat.total_folders + 1,
                                id_author=get_user_id(request),
                                name=folder_name,
                                date=date)              # new version

            # Обновляем статистику
            stat.total_folders += 1

            # Сохраняем все изменения в БД
            user.save()
            stat.save()
            new_folder.save()

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
        # path_publ = request.POST.get('answer')
        # user_data = check_auth(request)
        #
        #
        # try:
        #     user = User.objects.get(email=user_data)
        #     wt = WikiTree(user.id_user)
        #     wt.load_tree(user.tree)
        #
        #     if wt.check_folder_for_delete(path_publ.split(":")[0]):
        #         wt.delete_folder(path_publ.split(":")[0])
        #         user.tree = wt.get_tree()
        #         user.save()
        #         return HttpResponse('ok', content_type='text/html')
        #     else:
        #         return HttpResponse('no', content_type='text/html')
        #
        # except User.DoesNotExist:
        #     return HttpResponse('no', content_type='text/html')
        return HttpResponse('ok', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_check_folder_for_delete(request):
    """Ajax представление. Проверка папку на пустоту, для ее удаления"""

    if request.method == "POST":
        # path_publ = request.POST.get('answer')
        # user_data = check_auth(request)
        #
        #
        # try:
        #     user = User.objects.get(email=user_data)
        #     wt = WikiTree(user.id_user)
        #     wt.load_tree(user.tree)
        #
        #     if wt.check_folder_for_delete(path_publ.split(":")[0]):
        #         return HttpResponse('ok', content_type='text/html')
        #     else:
        #         return HttpResponse('no', content_type='text/html')
        #
        # except User.DoesNotExist:
        #     return HttpResponse('no', content_type='text/html')
        return HttpResponse('ok', content_type='text/html')

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
            wft = WikiFileTree()
            # Загружаем его дерево
            wft.load_tree(user.file_tree)
            # Удаляем публикацию по указанному id
            wft.delete_publication(int(id_publ))
            user.file_tree = wft.get_xml_str()

            # Уменьшаем количество публикаций у пользователя
            user.publications -= 1

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
        id = arr[1]

        try:
            user = User.objects.get(email=user_data)
            publication = Publication.objects.get(id_publication=id)
            wft = WikiFileTree()
            wft.load_tree(user.file_tree)
            wft.rename_publication(int(id), new_name_publ)

            publication.title = new_name_publ
            user.file_tree = wft.get_xml_str()

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
        answer = request.POST.get('answer')
        user_data = check_auth(request)
        arr = str(answer).split("^^^")
        new_name_folder = arr[0]
        id = arr[1]

        try:
            user = User.objects.get(email=user_data)
            folder = Folder.objects.get(id_folder=id)
            wft = WikiFileTree()
            wft.load_tree(user.file_tree)
            wft.rename_folder(id, new_name_folder)

            folder.name = new_name_folder
            user.file_tree = wft.get_xml_str()

            # Сохраняем все изменения в БД
            user.save()
            folder.save()

            return HttpResponse('ok', content_type='text/html')
        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')
        except Folder.DoesNotExist:
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
        id_publ = int(publ)

        try:
            user = User.objects.get(id_user=user_id)
            user.preview_publ_id = id_publ
            user.save()
            return HttpResponse('ok', content_type='text/html')
        except User.DoesNotExist:
            return HttpResponse('no', content_type='text/html')

    else:
        return HttpResponse('no', content_type='text/html')


def get_remove_saved(request):
    if request.method == "POST":

        # Получаем конспект, который хотим удалить
        try:
            saved_id = int(request.POST.get("saved_id_publ"))

            publication = Publication.objects.get(id_publication=saved_id)

            # Получаем текущего пользователя
            cur_user = User.objects.get(id_user=get_user_id(request))

            # Получаем файловое дерево пользователя
            wft = WikiFileTree()
            wft.load_tree(cur_user.file_tree)
            if not wft.is_publication(saved_id):
                return get_tree_manager(request, notify={'type': 'error', 'text': 'Данного конспекта не существует, '
                                                                                  'либо он уже удален.'})

            wft.delete_publication(saved_id)
            publication.saves -= 1
            publication.stars -= 1
            cur_user.file_tree = wft.get_xml_str()
            cur_user.save()
            publication.save()

            return get_tree_manager(request, notify={'type': 'info', 'text': 'Конспект успешно удален из сохраненных.'})
        except User.DoesNotExist:
            return get_error_page(request, ["User not found"])
        except Publication.DoesNotExist:
            return get_error_page(request, ["Publication not found"])
        except:
            return get_tree_manager(request, notify={'type': 'error', 'text': 'Не удалось удалить конспект.'})
    else:
        return get_tree_manager(request, notify={'type': 'error', 'text': 'Не удалось удалить конспект.'})


def get_move_publication(request):
    if request.method == "POST":

        try:

            # Получаем конспект, который хотим переместить
            moved_id = int(request.POST.get("current-pubication-id"))

            # Получаем папку, в которую хотим переместить конспект
            to_folder_id = int(request.POST.get("move-publ-path-folder").split(":")[1])

            # Получаем текущего пользователя
            cur_user = User.objects.get(id_user=get_user_id(request))

            # Получаем файловое дерево пользователя
            wft = WikiFileTree()
            wft.load_tree(cur_user.file_tree)
            if not wft.is_publication(moved_id):
                return get_tree_manager(request, notify={'type': 'error', 'text': 'Данного конспекта не существует, '
                                                                                  'либо он уже удален.'})
            wft.move_publication(moved_id, to_folder_id)
            cur_user.file_tree = wft.get_xml_str()
            cur_user.save()

            return get_tree_manager(request, notify={'type': 'info', 'text': 'Конспект успешно перемещен.'})
        except User.DoesNotExist:
            return get_error_page(request, ["User not found"])
        except:
            return get_tree_manager(request, notify={'type': 'error', 'text': 'Не удалось переместить конспект.'})
    else:
        return get_tree_manager(request, notify={'type': 'error', 'text': 'Не удалось переместить конспект.'})
