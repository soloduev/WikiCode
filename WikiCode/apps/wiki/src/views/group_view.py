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

from django.http import HttpResponse
from django.shortcuts import render, redirect
from WikiCode.apps.wiki.models import Group, User, Publication
from WikiCode.apps.wiki.src.modules.wiki_permissions.wiki_permissions import WikiPermissions
from WikiCode.apps.wiki.src.modules.wiki_tree.wiki_tree import WikiFileTree
from WikiCode.apps.wiki.src.views.auth import check_auth, get_user_id
from WikiCode.apps.wiki.src.views.error_view import get_error_page


def get_group(request, id, notify=None):
    """ Возвращает страницу группы.
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
        # Получаем группу
        group = Group.objects.get(id_group=id)
        # Получаем автора группы
        author = User.objects.get(id_user=group.id_author)
        # Получаем превью дерево группы
        wft = WikiFileTree()
        wft.load_tree(author.file_tree)
        preview_tree = wft.to_html_preview_concrete_folder(id)
        # Получаем файловое дерево для выбора превью конспекта
        dynamic_tree = wft.to_html_dynamic_concrete_folder(id)
        # Получаем путь к превью конспекту если он есть
        if group.preview_publ_id != -1:
            preview_publ_path = wft.get_path_publ(group.preview_publ_id)
            preview_publ_path_value = "publ:" + str(group.preview_publ_id)
        else:
            preview_publ_path = ""
            preview_publ_path_value = ""
        # Получаем все теги группы

        # Получаем всех участников группы

        # Получаем превью конспект группы
        preview_publ_text = None
        preview_publ_id = None
        try:
            if group.preview_publ_id != -1:
                preview_publ = Publication.objects.get(id_publication=group.preview_publ_id)
                preview_publ_text = preview_publ.text
                preview_publ_id = preview_publ.id_publication
        except Publication.DoesNotExist:
            pass
        # Получаем оглавление группы

        # Получаем список последних конспектов группы

        if str(get_user_id(request)) == str(group.id_author):
            # Отрисовываем группу глазами автора

            context = {
                "user_data": user_data,
                "user_id": get_user_id(request),
                "is_author": True,
                "author_nickname": author.nickname,
                "group": group,
                "tags": "",
                "total_publs": 0,
                "total_members": 0,
                "preview_tree": preview_tree,
                "dynamic_tree": dynamic_tree,
                "preview_publ_text": preview_publ_text,
                "preview_publ_id": preview_publ_id,
                "preview_publ_path": preview_publ_path,
                "preview_publ_path_value": preview_publ_path_value
            }

            return render(request, 'wiki/group.html', context)

        else:
            # Отрисовываем группу другого пользователя

            context = {
                "user_data": user_data,
                "user_id": get_user_id(request),
                "is_author": False,
                "author_nickname": author.nickname,
                "group": group,
                "tags": "",
                "total_publs": 0,
                "total_members": 0,
                "preview_tree": preview_tree,
                "dynamic_tree": dynamic_tree,
                "preview_publ_text": preview_publ_text,
                "preview_publ_id": preview_publ_id,
                "preview_publ_path": preview_publ_path,
                "preview_publ_path_value": preview_publ_path_value
            }

            return render(request, 'wiki/group.html', context)
    except Group.DoesNotExist:
        return get_error_page(request, ["Группы с таким id не существует!"])
    except User.DoesNotExist:
        context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
        }
        return render(request, 'wiki/create.html', context)


def create_group(request):
    if request.method == "POST":
        # Проверяем, аутентифицирован ли пользователь
        if get_user_id(request) == -1:
            return HttpResponse('no', content_type='text/html')
        else:
            try:
                # Получаем все значения с формы
                title_group = request.POST.get("title-group")
                type_group = request.POST.get("type-group")
                description_group = request.POST.get("description-group")
                permission_group = request.POST.get("permission-group")
                status_group = request.POST.get("status-group")
                folder_id_group = int(request.POST.get("create-group-folder").split(":")[1])

                if not title_group or not type_group or not permission_group or not folder_id_group:
                    return render(request, 'wiki/tree_manager.html', {})

                # Создаем группу.
                # Проверяем, не существует ли уже такая группы
                try:
                    group = Group.objects.get(id_group=folder_id_group)
                    return render(request, 'wiki/group.html', {})
                except Group.DoesNotExist:

                    wp = WikiPermissions()
                    wp.create_permissions(folder_id_group, get_user_id(request))

                    # Получаем текущую дату
                    date = str(datetime.datetime.now())
                    date = date[:len(date) - 7]

                    # Создаем новую группу
                    group = Group(id_group=folder_id_group,
                                  id_author=get_user_id(request),
                                  title=title_group,
                                  type=type_group,
                                  description=description_group,
                                  status=status_group,
                                  members=wp.get_xml_str(),
                                  date_create=date,
                                  rating=0,
                                  tags="",
                                  preview_publ_id=-1)

                    # Получаем текущего пользователя
                    cur_user = User.objects.get(id_user=get_user_id(request))

                    # Загружаем файловое дерево пользователя
                    wft = WikiFileTree()
                    wft.load_tree(cur_user.file_tree)

                    # Конвертация типа папки
                    if type_group == "Группа":
                        type_group = "group"
                    elif type_group == "Документация":
                        type_group = "doc"
                    elif type_group == "Курс":
                        type_group = "course"
                    elif type_group == "Организация":
                        type_group = "org"

                    # Меняем тип папки
                    wft.retype_folder(folder_id_group, type_group)

                    # Сохраняем все изменения
                    cur_user.file_tree = wft.get_xml_str()
                    cur_user.save()
                    group.save()

                    return get_group(request, folder_id_group)
            except User.DoesNotExist:
                return get_error_page(request, ["User not found!"])
    else:
        return get_error_page(request, ["Error in create_group."])


def get_save_group(request, id):
    """ Сохранение настроек группы """
    if request.method == "POST":
        # Проверяем, аутентифицирован ли пользователь
        if get_user_id(request) == -1:
            return HttpResponse('no', content_type='text/html')
        else:
            try:
                # Получаем все значения с формы
                title_group = request.POST.get("title-group")
                type_group = request.POST.get("type-group")
                description_group = request.POST.get("description-group")
                permission_group = request.POST.get("permission-group")
                status_group = request.POST.get("status-group")
                preview_publ_id = request.POST.get("preview-publ-group")
                if preview_publ_id:
                    preview_publ_id = int(preview_publ_id.split(":")[1])
                else:
                    preview_publ_id = -1

                # Получаем текущего пользователя
                cur_user = User.objects.get(id_user=get_user_id(request))

                # Загружаем файловое дерево пользователя
                wft = WikiFileTree()
                wft.load_tree(cur_user.file_tree)

                # Получаем текущую группу и применяем настройки
                cur_group = Group.objects.get(id_group=id)

                cur_group.title = title_group if title_group.strip() != "" else cur_group.title
                cur_group.type = type_group

                # Конвертация типа папки
                if type_group == "Группа":
                    type_group = "group"
                elif type_group == "Документация":
                    type_group = "doc"
                elif type_group == "Курс":
                    type_group = "course"
                elif type_group == "Организация":
                    type_group = "org"

                # Меняем тип папки
                wft.retype_folder(id, type_group)

                # Сохраняем все изменения
                cur_user.file_tree = wft.get_xml_str()

                cur_group.description = description_group
                cur_group.status = status_group
                cur_group.preview_publ_id = preview_publ_id

                cur_group.save()
                cur_user.save()

                return redirect('/group/' + str(id) + '/')
            except Group.DoesNotExist:
                return get_error_page(request, ["Group is not found."])
            except User.DoesNotExist:
                return get_error_page(request, ["User is not found."])
            except:
                return get_error_page(request, ["Error in save_group."])
    else:
        return get_error_page(request, ["Error in save_group."])


def get_save_group_show(request, id):
    """ Сохранение настроек отображения группы """
    if request.method == "POST":
        # Проверяем, аутентифицирован ли пользователь
        if get_user_id(request) == -1:
            return HttpResponse('no', content_type='text/html')
        else:
            try:
                # Получаем все значения с формы
                show_total_publs = request.POST.get("show-total-publs", False)
                show_total_members = request.POST.get("show-total-members", False)
                show_rating = request.POST.get("show-rating", False)
                show_date = request.POST.get("show-date", False)
                show_preview_tree = request.POST.get("show-preview-tree", False)
                show_status = request.POST.get("show-status", False)
                show_description = request.POST.get("show-description", False)
                show_tags = request.POST.get("show-tags", False)
                show_conents = request.POST.get("show-conents", False)
                show_members = request.POST.get("show-members", False)
                show_author = request.POST.get("show-author", False)

                # Получаем текущую группу и применяем настройки
                cur_group = Group.objects.get(id_group=id)
                cur_group.is_show_total_members = show_total_members
                cur_group.is_show_total_publ = show_total_publs
                cur_group.is_show_rating = show_rating
                cur_group.is_show_date = show_date
                cur_group.is_show_preview_tree = show_preview_tree
                cur_group.is_show_status = show_status
                cur_group.is_show_description = show_description
                cur_group.is_show_tags = show_tags
                cur_group.is_show_contents = show_conents
                cur_group.is_show_members = show_members
                cur_group.is_show_author = show_author

                cur_group.save()

                return redirect('/group/' + str(id) + '/')
            except Group.DoesNotExist:
                return get_error_page(request, ["Group is not found."])
            except:
                return get_error_page(request, ["Error in save_group_show."])
    else:
        return get_error_page(request, ["Error in save_group_show."])