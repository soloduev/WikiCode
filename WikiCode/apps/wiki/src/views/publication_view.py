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
import json

from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt

import configuration as wiki_settings
from WikiCode.apps.wiki.models import Publication, Statistics, Folder
from WikiCode.apps.wiki.models import User
from WikiCode.apps.wiki.src.engine import wcode
from WikiCode.apps.wiki.src.fs.fs import WikiFileSystem
from WikiCode.apps.wiki.src.wiki_markdown import WikiMarkdown
from .auth import check_auth, get_user_id


def get_create(request):
    user_data = check_auth(request)
    try:
        # Получения id папки, в которой хотим создать конспект
        input_folder_id = ""
        path_folder = ""
        full_path = str(request.POST.get('folder_publ'))

        user = User.objects.get(email=user_data)

        wft = WikiFileSystem()
        wft.load_tree(user.file_tree)

        if full_path != "None" and full_path != "NONE":
            input_folder_id = full_path
            path_folder = wft.get_path_folder(int(full_path.split(":")[1]))

        # Проверяем, не пустует ли его дерево:
        if wft.get_num_root_folders() == 0:
            empty_tree = True
        else:
            empty_tree = False

        context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
            "dynamic_tree": wft.to_html_dynamic_folders(),
            "path": input_folder_id,
            "show_path": path_folder,
            "empty_tree": empty_tree,
        }

        return render(request, 'wiki/create.html', context)
    except User.DoesNotExist:
        context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
        }
        return render(request, 'wiki/create.html', context)


def get_page(request, id):
    """ Возвращает страницу конспекта."""

    try:
        cur_user_id = get_user_id(request)
        publication = Publication.objects.get(id_publication=id)

        try:
            user = User.objects.get(id_user=publication.id_author)
            wft = WikiFileSystem()
            wft.load_tree(user.file_tree)
        except User.DoesNotExist:
            return wcode.goerror(request, ["Не удалось загрузить юзера. Его уже не существует!"])

        # Разбиваем весь текст на абзацы
        md_text = publication.text
        wm = WikiMarkdown()
        arr = wm.split(md_text)
        numbers = []
        paragraphs = []
        for i in range(0, len(arr)):
            numbers.append(str(i + 1))
            paragraphs.append({
                "index": str(i + 1),
                "text": arr[i]
            })

        # Загружаем превью дерево автора
        try:
            author_user = User.objects.get(id_user=publication.id_author)

            wft = WikiFileSystem()
            wft.load_tree(author_user.file_tree)
            if author_user.id_user == cur_user_id:
                html_preview_tree = wft.to_html_preview()
            else:
                html_preview_tree = wft.to_html_preview(only_public=True)
        except User.DoesNotExist:
            print("Автора не существует")

        # Генерируем оглавление для конспекта
        contents = wm.generate_contents(paragraphs, publication.id_publication)

        # Получаем файловое дерево пользователя, для сохранения конспекта
        try:
            if cur_user_id != -1:
                cur_user = User.objects.get(id_user=cur_user_id)
                wft = WikiFileSystem()
                wft.load_tree(cur_user.file_tree)
                dynamic_tree = wft.to_html_dynamic_folders()
            else:
                dynamic_tree = None
        except User.DoesNotExist:
            return wcode.goerror(request, ["Пользователя не сущесвует"])

        context = {
            "publication": publication,
            "paragraphs": paragraphs,
            "numbers": numbers,
            "user_data": check_auth(request),
            "user_id": cur_user_id,
            "preview_tree": html_preview_tree,
            "dynamic_tree": dynamic_tree,
            "module_dynamic_paragraphs": wiki_settings.MODULE_DYNAMIC_PARAGRAPHS,
            "module_main_comments": wiki_settings.MODULE_MAIN_COMMENTS,
            "module_versions": wiki_settings.MODULE_VERSIONS,
            "contents": contents,
            "is_editable": author_user.id_user == cur_user_id
        }

        return render(request, 'wiki/page/page.html', context)
    except Publication.DoesNotExist:
        return wcode.goerror(request, ["This is publication not found!", "Page not found: page/" + str(id) + "/"])


def get_create_page(request):
    # Получаем данные формы
    form = request.POST
    # Получаем пользователя
    user_data = check_auth(request)
    try:
        user = User.objects.get(email=user_data)
    except User.DoesNotExist:
        return wcode.goerror(request, ["Пользователя, создающего конспект не существует!"])
    # Проверяем, чего хотим сделать
    if request.POST.get('secret') == "off":
        with open("WikiCode/apps/wiki/generate_pages/gen_page.gen", "r", encoding='utf-8') as f:
            gen_page = f.read()
        first_part = "<!DOCTYPE html><html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"><title>" + \
                     form["title"] + '</title></head><xmp theme="' + form[
                         "theme"].lower() + '" style="display:none;">'
        second_part = form["text"]
        ready_page = first_part + second_part + gen_page
        stat = Statistics.objects.get(id_statistics=1)
        num = stat.publications_create
        stat.publications_create += 1

        newid = num + 1

        # Перед тем, как создать публикацию, проверяем, не существует ли она уже
        try:
            publ = Publication.objects.get(id_publication=newid)
            return wcode.goerror(request, ["Конспект с таким id уже существует!"])
        except Publication.DoesNotExist:

            new_publication = Publication(
                id_publication=newid,
                id_author=user.id_user,
                nickname_author=user.nickname,
                title=form["title"],
                description=form["description"],
                text=form["text"],
                theme=form["theme"],
                tree_path=form["folder"],
                read=0,
                saves=0,
                is_public=request.POST.get("access-opt", False),
                is_dynamic_paragraphs=request.POST.get("dynamic-opt", False),
                is_show_author=request.POST.get("show-author-opt", False),
                is_loading=request.POST.get("loading-opt", False),
                is_saving=request.POST.get("saving-opt", False),
                is_file_tree=request.POST.get("file-tree-opt", False)
            )

        # Загружаем дерево пользователя
        wft = WikiFileSystem()
        wft.load_tree(user.file_tree)

        # Добавляем этот конспект в папку
        wft.create_publication(id=newid,
                               name=form["title"],
                               access="public" if request.POST.get("access-opt", False) else "private",
                               type="personal",
                               id_folder=form['folder'].split(':')[1])  # new version

        user.file_tree = wft.get_xml_str()  # new version

        # Сохраняем все новые данные:

        # Статистика
        stat.save()

        # Конспект
        new_publication.save()

        # Пользователь
        user.save()

        return HttpResponseRedirect("/")
    else:
        first_part = '<!DOCTYPE html><html><title>' + form["title"] + '</title><xmp theme="' + form[
            "theme"].lower() + '" style="display:none;">'
        second_part = form["text"]
        third_part = '</xmp><script src="http://strapdownjs.com/v/0.2/strapdown.js"></script></html>'
        total = first_part + second_part + third_part
        return HttpResponse(total)


def get_presentation(request, id):
    # Получаем данные формы
    try:
        publication = Publication.objects.get(id_publication=id)
        # Составляем страницу презентации конспекта
        first_part = '<!DOCTYPE html><html><title>' + publication.title + '</title><xmp theme="' + publication.theme.lower() + '" style="display:none;">'
        second_part = publication.text
        third_part = '</xmp><script src="http://strapdownjs.com/v/0.2/strapdown.js"></script></html>'
        total = first_part + second_part + third_part
        return HttpResponse(total)
    except Publication.DoesNotExist:
        return wcode.goerror(request, ["This is publication not found!"])


def get_publ_manager(request, id):
    """Запускает страницу управления конспектом"""

    try:
        # Получаем пользователя
        user_data = check_auth(request)

        # Получаем конспект, который хотим управлять
        _publication = Publication.objects.get(id_publication=id)

        # Проверяем, является ли автором этого конспекта тот пользователь
        # Который захотел управлять этим конспектом
        current_id = get_user_id(request)
        if current_id == _publication.id_author:

            # Получаем путь к конспекту
            cur_user = User.objects.get(id_user=current_id)
            id_folder = int(_publication.tree_path.split(":")[1])
            wft = WikiFileSystem()
            wft.load_tree(cur_user.file_tree)
            path_to_folder = wft.get_path_folder(id_folder)

            context = {
                "user_data": user_data,
                "user_id": current_id,
                "publication": _publication,
                "path_to_folder": path_to_folder,
            }
            return render(request, 'wiki/publ_manager.html', context)
        else:
            return wcode.goerror(request,
                                 ["Вы не являетесь автором данного конспекта, чтобы перейти в панель управления!"])

    except Publication.DoesNotExist:
        return wcode.goerror(request,
                             ["This is publication not found!", "Page not found: publ_manager/" + str(id) + "/"])
    except User.DoesNotExist:
        return wcode.goerror(request, ["User not found!"])
    except:
        return wcode.goerror(request, ["Ошибка перехода на страницу управления конспектом."])


@csrf_protect
def get_save_publication(request, id):
    """Ajax представление. Сохранение изменений в конспекте."""

    if request.method == "POST":
        # Проверяем, аутентифицирован ли пользователь
        if get_user_id(request) == -1:
            return HttpResponse('no', content_type='text/html')
        else:
            # Если пользователь аутентифицирован то, начинаем получать все изменения
            try:
                # Получаем текущую публикацию
                publication = Publication.objects.get(id_publication=id)
                # Получаем пользователя, оставляющего комментарий
                current_user = User.objects.get(id_user=get_user_id(request))
                # Получаем количество абзацев
                count_paragraphs = int(request.POST.get("count_paragraphs"))
                # Получаем абзацы
                md_text = ""
                for i in range(0, count_paragraphs):
                    md_text += request.POST.get(str(i + 1))
                wiki_markdown = WikiMarkdown()
                md_paragraphs = wiki_markdown.split(md_text)

                # Сверяем с теми, что есть на данный момент:
                current_paragraphs = wiki_markdown.split(publication.text)
                if len(current_paragraphs) == len(md_paragraphs):
                    equals = True
                    for i in range(0, len(current_paragraphs)):
                        if current_paragraphs[i] != md_paragraphs[i]:
                            equals = False
                            break
                    if equals:
                        return HttpResponse('eq', content_type='text/html')
                    else:
                        return HttpResponse('not_eq', content_type='text/html')
                else:
                    return HttpResponse('not_eq', content_type='text/html')

            except Publication.DoesNotExist:
                return wcode.goerror(request, ["This is publication not found!",
                                               "Page not found: publ_manager/" + str(id) + "/"])
    else:
        return HttpResponse('no', content_type='text/html')


def get_save_page(request, id):
    """ Сохранение конспекта в свое дерево конспектов """
    if request.method == "POST":
        # Проверяем, аутентифицирован ли пользователь
        if get_user_id(request) == -1:
            return HttpResponse('auth', content_type='text/html')
        else:
            # Если пользователь аутентифицирован то, начинаем получать все изменения
            try:
                # Получаем текущую публикацию
                publication = Publication.objects.get(id_publication=id)
                # Получаем пользователя, который собирается произвести сохранение конспекта
                current_user = User.objects.get(id_user=get_user_id(request))
                # Если этот пользователь не является автором данного конспекта:
                if current_user.id_user != publication.id_author:
                    # Получаем дерево конспектов пользователя
                    wft = WikiFileSystem()
                    wft.load_tree(current_user.file_tree)
                    # Получаем папку, в которую необходимо сохранить конспект
                    save_folder = request.POST.get("save_folder")
                    try:
                        # Получаем id папки в которую собираемся сохранить конспект
                        id_folder = int(save_folder.strip(" \n\r\t").split(":")[1])

                        # Проверяем, существует ли такая папка:
                        Folder.objects.get(id_folder=id_folder)

                        # Проверяем, сохранил ли пользователь у себя уже этот конспект
                        if wft.is_publication(publication.id_publication):

                            return wcode.goto('/page/' + str(id))

                        # Если такая папка существует сохраняем в нее этот конспект
                        wft.create_publication(id=publication.id_publication,
                                               name=publication.title,
                                               access="public",
                                               type="saved",
                                               id_folder=id_folder)

                        publication.saves += 1
                        publication.stars += 1
                        current_user.file_tree = wft.get_xml_str()
                        current_user.save()
                        publication.save()

                        return wcode.goto('/page/' + str(id))
                    except Folder.DoesNotExist:
                        return wcode.goerror(request, ["Такой папки не существует"])
                    except:
                        return wcode.goerror(request, ["Передан неверный формат пути к папке"])

                else:
                    return wcode.goerror(request, ["Вы являетесь автором данного конспекта, "
                                                   "Вы не можете его сохранить!"])
            except Publication.DoesNotExist:
                return wcode.goerror(request, ["This is publication not found!",
                                               "Page not found: publ_manager/" + str(id) + "/"])
    else:
        return HttpResponse('no', content_type='text/html')


@csrf_exempt
def get_load_md(request, id):
    """ Загрузка конспекта в формате markdown """
    if request.method == "POST":
        # Проверяем, аутентифицирован ли пользователь
        if get_user_id(request) == -1:
            return HttpResponse('auth', content_type='text/html; charset=utf8')
        else:
            # Если пользователь аутентифицирован то, начинаем получать все изменения
            try:
                # Получаем текущую публикацию
                publication = Publication.objects.get(id_publication=id)

                response = StreamingHttpResponse(publication.text)
                response['Content-Type'] = 'text/plain; charset=utf8'
                return response

            except User.DoesNotExist:
                return wcode.goerror(request, ["User not found."])
            except Publication.DoesNotExist:
                return wcode.goerror(request, ["This is publication not found!",
                                               "Page not found: publ_manager/" + str(id) + "/"])
    else:
        return wcode.goerror(request, ["По техническим причинам, вы пока не можете скачать этот конспект."])


def get_get_path_to_folder(request):
    """ Получение полного пути к папке """
    if request.method == "GET":
        # Проверяем, аутентифицирован ли пользователь
        if get_user_id(request) == -1:
            return HttpResponse('auth', content_type='text/html; charset=utf8')
        else:
            # Если пользователь аутентифицирован то, начинаем получать все изменения
            try:
                # Получаем папку, к которой необходимо получить путь
                id_folder = int(request.GET.get('id_folder'))
                # Получаем пользователя
                cur_user = User.objects.get(id_user=get_user_id(request))

                # Получаем путь к папке
                wft = WikiFileSystem()
                wft.load_tree(cur_user.file_tree)
                folder_path = wft.get_path_folder(id_folder)

                if folder_path is not None:
                    return HttpResponse(folder_path, content_type='text/html')
                else:
                    return HttpResponse('no', content_type='text/html')
            except User.DoesNotExist:
                return wcode.goerror(request, ["User not found."])
            except:
                return HttpResponse('no', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')


def get_get_path_to_publ(request, id):
    """ Получение полного пути к конспекту """
    if request.method == "GET":
        # Проверяем, аутентифицирован ли пользователь
        if get_user_id(request) == -1:
            return HttpResponse('auth', content_type='text/html; charset=utf8')
        else:
            # Если пользователь аутентифицирован то, начинаем получать все изменения
            try:
                # Получаем конспект, к которой необходимо получить путь
                id_publ = int(request.GET.get('id_publ'))
                # Получаем пользователя
                cur_user = User.objects.get(id_user=get_user_id(request))

                # Получаем путь к конспекту
                wft = WikiFileSystem()
                wft.load_tree(cur_user.file_tree)
                publ_path = wft.get_path_publ(id_publ)

                if publ_path is not None:
                    return HttpResponse(publ_path, content_type='text/html')
                else:
                    return HttpResponse('no', content_type='text/html')
            except User.DoesNotExist:
                return wcode.goerror(request, ["User not found."])
            except:
                return HttpResponse('no', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')
