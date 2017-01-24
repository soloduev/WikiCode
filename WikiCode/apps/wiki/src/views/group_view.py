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
from WikiCode.apps.wiki.src.api import wcode


def get_group(request, id):
    """ Возвращает страницу группы."""

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
        wp = WikiPermissions()
        wp.load_permissions(group.members)
        white_list = wp.get_white_list()
        black_list = wp.get_black_list()

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

        # Получаем список последних id конспектов группы
        all_publs_id = wft.get_publications_id(int(id))
        # Получаем реальный список конспектов
        all_publs = []
        for id in all_publs_id:
            try:
                publ = Publication.objects.get(id_publication=id)
                all_publs.append(publ)
            except Publication.DoesNotExist:
                pass

        if str(get_user_id(request)) == str(group.id_author):
            # Отрисовываем группу глазами автора

            context = {
                "user_data": check_auth(request),
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
                "preview_publ_path_value": preview_publ_path_value,
                "all_publs": all_publs,
                "notify": wcode.notify.instant.get(request),
                "white_list": white_list,
                "black_list": black_list
            }

            return render(request, 'wiki/group.html', context)

        else:
            # Отрисовываем группу другого пользователя

            context = {
                "user_data": check_auth(request),
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
                "preview_publ_path_value": preview_publ_path_value,
                "all_publs": all_publs,
                "notify": wcode.notify.instant.get(request),
                "white_list": white_list,
                "black_list": black_list
            }

            return render(request, 'wiki/group.html', context)
    except Group.DoesNotExist:
        return get_error_page(request, ["Группы с таким id не существует!"])
    except User.DoesNotExist:
        context = {
            "user_data": check_auth(request),
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

                    return wcode.goto('/group/' + str(folder_id_group))
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


def get_add_member_group(request, id):
    if request.method == "POST":
        try:
            # Получаем группу, которой хотим управлять
            group = Group.objects.get(id_group=id)

            white_user = request.POST.get("add_member_group")

            try:
                find_user = User.objects.get(nickname=white_user)

                if find_user.id_user == get_user_id(request):
                    wcode.notify.instant.create(request, "error", 'Вы и так являетесь автором данной группы.\n'
                                                                  'Вы не можете назначить себя участником.\n\n')
                    return wcode.goto('/group/' + str(id))

                wp = WikiPermissions()
                wp.load_permissions(group.members)
                white_users = wp.get_white_list()
                black_users = wp.get_black_list()

                # Проверяем пользователя на его наличие в белом списке
                is_find = False
                for user in white_users:
                    if str(find_user.id_user) == str(user["id"]):
                        is_find = True

                # Проверяем пользователя на его наличие в черном списке
                is_find_black = False
                for user in black_users:
                    if str(find_user.id_user) == str(user["id"]):
                        is_find_black = True

                if is_find_black:
                    wcode.notify.instant.create(request,
                                                "error", 'Данный пользователь уже находится у Вас в черном списке.\n'
                                                         'Удалите его из черного списка, если хотите назначить его '
                                                         'участником\n\n')
                    return wcode.goto('/group/' + str(id))

                if not is_find:
                    wp.add_to_white_list(find_user.id_user, find_user.nickname, "member", "Участник")
                    group.members = wp.get_xml_str()
                    group.save()

                    wcode.notify.instant.create(request, "info", 'Добавлен новый участник группы.\n\n\n')

                    return wcode.goto('/group/' + str(id))
                else:
                    wcode.notify.instant.create(request, "error", 'Данный пользователь уже назначен участником.\n\n\n')
                    return wcode.goto('/group/' + str(id))

            except User.DoesNotExist:
                wcode.notify.instant.create(request, "error", 'Пользователя с таким nickname не существует.\n'
                                                              'Новый участник не назначен.\n\n')
                return wcode.goto('/group/' + str(id))

        except Group.DoesNotExist:
            return get_error_page(request,
                                  ["This is group not found!", "Group not found: group/" + str(id) + "/"])


def get_del_member_group(request, id):
    if request.method == "POST":
        try:
            # Получаем группу, которой хотим управлять
            group = Group.objects.get(id_group=id)

            del_member_nickname = request.POST.get("member-group")

            if not del_member_nickname:
                wcode.notify.instant.create(request, "error", 'Вы не указали удаляемого пользователя.\n\n\n')
                return wcode.goto('/group/' + str(id))

            try:
                find_user = User.objects.get(nickname=del_member_nickname)

                wp = WikiPermissions()
                wp.load_permissions(group.members)
                white_users = wp.get_white_list()
                is_find = False
                for user in white_users:
                    if str(find_user.id_user) == str(user["id"]):
                        is_find = True

                if is_find:
                    wp.remove_from_white_list(find_user.id_user)
                    group.members = wp.get_xml_str()
                    group.save()

                    wcode.notify.instant.create(request, "info",
                                                'Пользователь успешно удален из списка участников.\n\n\n')
                    return wcode.goto('/group/' + str(id))
                else:
                    wcode.notify.instant.create(request, "error",
                                                'Пользователь уже удален из списка участников\n\n\n')
                    return wcode.goto('/group/' + str(id))

            except User.DoesNotExist:
                wcode.notify.instant.create(request, "error",
                                            'Удаляемого пользователя не существует.\n\n\n')
                return wcode.goto('/group/' + str(id))

        except Group.DoesNotExist:
            return get_error_page(request,
                                  ["This is group not found!", "Group not found: group/" + str(id) + "/"])


def get_add_black_user_group(request, id):
    if request.method == "POST":
        try:
            # Получаем группу, которой хотим управлять
            group = Group.objects.get(id_group=id)

            black_user = request.POST.get("add_black_user_group")

            try:
                find_user = User.objects.get(nickname=black_user)

                if find_user.id_user == get_user_id(request):
                    wcode.notify.instant.create(request, "error", 'Вы не можете себя добавить в черный список.\n\n\n')
                    return wcode.goto('/group/' + str(id))

                wp = WikiPermissions()
                wp.load_permissions(group.members)
                black_users = wp.get_black_list()
                white_users = wp.get_white_list()

                is_find = False
                for user in black_users:
                    if str(find_user.id_user) == str(user["id"]):
                        is_find = True

                # Проверяем пользователя на его наличие в белом списке
                is_find_white = False
                for user in white_users:
                    if str(find_user.id_user) == str(user["id"]):
                        is_find_white = True

                if is_find_white:
                    wcode.notify.instant.create(request,
                                                "error",
                                                'Данный пользователь является участником '
                                                'Вашей группы.\n'
                                                'Удалите его из списка участников, если хотите добавить его'
                                                ' в черный список\n\n')
                    return wcode.goto('/group/' + str(id))

                if not is_find:
                    wp.add_to_black_list(find_user.id_user, find_user.nickname, "ban", "Бан")
                    group.members = wp.get_xml_str()
                    group.save()

                    wcode.notify.instant.create(request, "info", 'Пользователь добавлен в черный список.\n\n\n')

                    return wcode.goto('/group/' + str(id))
                else:
                    wcode.notify.instant.create(request, "error",
                                                'Данный пользователь уже добавлен в черный список.\n\n\n')
                    return wcode.goto('/group/' + str(id))

            except User.DoesNotExist:
                wcode.notify.instant.create(request, "error",
                                                     'Пользователя с таким nickname не существует.\n'
                                                     'Пользователь не добавлен в черный список.\n\n')
                return wcode.goto('/group/' + str(id))

        except Group.DoesNotExist:
            return get_error_page(request,
                                  ["This is group not found!", "Group not found: group/" + str(id) + "/"])


def get_del_black_user_group(request, id):
    if request.method == "POST":
        try:
            # Получаем конспект, которым хотим управлять
            group = Group.objects.get(id_group=id)

            del_user_nickname = request.POST.get("black-list-group")

            if not del_user_nickname:
                wcode.notify.instant.create(request, "error", 'Вы не указали удаляемого пользователя.\n\n\n')
                return wcode.goto('/group/' + str(id))

            try:
                find_user = User.objects.get(nickname=del_user_nickname)

                wp = WikiPermissions()
                wp.load_permissions(group.members)
                black_users = wp.get_black_list()
                is_find = False
                for user in black_users:
                    if str(find_user.id_user) == str(user["id"]):
                        is_find = True

                if is_find:
                    wp.remove_from_black_list(find_user.id_user)
                    group.members = wp.get_xml_str()
                    group.save()

                    wcode.notify.instant.create(request, "info", 'Пользователь успешно удален из черного списка.\n\n\n')
                    return wcode.goto('/group/' + str(id))
                else:
                    wcode.notify.instant.create(request, "error", 'Пользователь уже удален из черного списка.\n\n\n')
                    return wcode.goto('/group/' + str(id))

            except User.DoesNotExist:
                wcode.notify.instant.create(request, "error", 'Удаляемого пользователя не существует.\n\n\n')
                return wcode.goto('/group/' + str(id))

        except Group.DoesNotExist:
            return get_error_page(request,
                                  ["This is group not found!", "Group not found: group/" + str(id) + "/"])


def get_del_group(request, id):
    """ Удаление группы """
    if request.method == "POST":
        try:
            # Получаем конспект, которым хотим управлять
            group = Group.objects.get(id_group=id)

            # Получаем текущего пользователя
            cur_user = User.objects.get(id_user=get_user_id(request))

            # Загружаем файловое дерево пользователя
            wft = WikiFileTree()
            wft.load_tree(cur_user.file_tree)

            # Меняем тип папки
            wft.retype_folder(id, "personal")

            # Сохраняем папки
            cur_user.file_tree = wft.get_xml_str()

            # Удаляем группу
            group.delete()
            cur_user.save()

            return wcode.goto('tree_manager')

        except Group.DoesNotExist:
            return get_error_page(request,
                                  ["This is group not found!", "Group not found: group/" + str(id) + "/"])
        except User.DoesNotExist:
            return get_error_page(request,
                                  ["This is user not found!", "User not found: user/" + str(get_user_id(request)) + "/"])
    else:
        return wcode.goto("tree_manager")
