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

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from WikiCode.apps.wiki.models import Publication, Statistics, Viewing
from WikiCode.apps.wiki.models import User
from WikiCode.apps.wiki.src.wiki_markdown import WikiMarkdown
from WikiCode.apps.wiki.src.wiki_tree import WikiTree
from WikiCode.apps.wiki.src.views.error_view import get_error_page
from WikiCode.apps.wiki.settings import wiki_settings
from .auth import check_auth, get_user_id


def get_create(request):
    user_data = check_auth(request)
    try:
        # Получения пути к папке, где хотим создать конспект
        path = ""
        full_path = str(request.POST.get('folder_publ'))

        if full_path != "None" and full_path != "NONE":
            path = full_path.split(":")[0]
            if path.count(".publ") == 1:
                path = path[:path.rfind("/")+1]
        user = User.objects.get(email=user_data)
        wt = WikiTree(user.id_user)
        wt.load_tree(user.tree)

        # Проверяем, не пустует ли его дерево:
        if wt.get_nums_root_folder() == 0:
            empty_tree = True
        else:
            empty_tree = False

        context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
            "dynamic_tree": wt.generate_html_dynamic_folders(),
            "path": path,
            "empty_tree":empty_tree,
        }

        return render(request, 'wiki/create.html', context)
    except User.DoesNotExist:
        context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
        }
        return render(request, 'wiki/create.html', context)


def get_page(request, id):
    try:
        cur_user_id = get_user_id(request)
        publication = Publication.objects.get(id_publication=id)

        try:
            user = User.objects.get(id_user=publication.id_author)
            wt = WikiTree(user.id_user)
            wt.load_tree(user.tree)
        except User.DoesNotExist:
            return get_error_page(request, ["Не удалось загрузить юзера. Его уже не существует!"])

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
            wt = WikiTree(author_user.id_user)
            wt.load_tree(author_user.tree)
            html_preview_tree = wt.generate_html_preview()
        except User.DoesNotExist:
            print("Автора не существует")

        # И перед тем как перейти на страницу, добавим ей просмотр, если этот пользователь еще не смотрел
        # Этот конспект
        try:
            viewing = Viewing.objects.get(id_user=cur_user_id, id_publ=id)
            # Просмотр стоит, ничего не добавляем
        except Viewing.DoesNotExist:
            # Просмотр не стоит. Ставим

            # Получаем текущую дату
            date = str(datetime.datetime.now())
            date = date[:len(date) - 7]

            new_viewing = Viewing(id_user=cur_user_id,
                                  nickname=user.nickname,
                                  id_publ=id,
                                  date=date)
            new_viewing.save()
            publication.read += 1
            publication.save()

        context = {
            "publication": publication,
            "paragraphs": paragraphs,
            "numbers": numbers,
            "user_data": check_auth(request),
            "user_id": cur_user_id,
            "preview_tree": html_preview_tree,
            "module_dynamic_paragraphs": wiki_settings.MODULE_DYNAMIC_PARAGRAPHS
        }

        return render(request, 'wiki/page.html', context)
    except Publication.DoesNotExist:
        return get_error_page(request, ["This is publication not found!", "Page not found: page/"+str(id)+"/"])


def get_create_page(request):
    # Получаем данные формы
    form = request.POST
    # Получаем пользователя
    user_data = check_auth(request)
    try:
        user = User.objects.get(email=user_data)
    except User.DoesNotExist:
        return get_error_page(request, ["Пользователя, создающего конспект не существует!"])
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
            return get_error_page(request,["Конспект с таким id уже существует!"])
        except Publication.DoesNotExist:
            new_publication = Publication(
                id_publication=newid,
                id_author=user.id_user,
                nickname_author=user.nickname,
                title=form["title"],
                description=form["description"],
                text=form["text"],
                theme=form["theme"],
                html_page=ready_page,
                tree_path=form["folder"]+form["title"]+".publ:"+str(newid),
                read=0)


        # Загружаем дерево пользователя
        wt = WikiTree(user.id_user)
        wt.load_tree(user.tree)
        # Добавляем этот конспект в папку
        wt.add_publication(form["folder"],form["title"],newid)
        user.tree = wt.get_tree()
        # Увеличиваем количество публикаций в статистике у пользователя
        user.publications += 1

        stat.save()
        new_publication.save()
        user.save()
        return HttpResponseRedirect("/")
    else:
        first_part = '<!DOCTYPE html><html><title>' + form["title"] + '</title><xmp theme="' + form[
            "theme"].lower() + '" style="display:none;">'
        second_part = form["text"]
        third_part = '</xmp><script src="http://strapdownjs.com/v/0.2/strapdown.js"></script></html>'
        total = first_part + second_part + third_part
        return HttpResponse(total)


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

            context = {
                "user_data": user_data,
                "user_id": current_id,
                "publication":_publication,
                "tree_path":_publication.tree_path.split(":")[0]
            }
            return render(request, 'wiki/publ_manager.html', context)
        else:
            return get_error_page(request, ["Вы не являетесь автором данного конспекта, чтобы перейти в панель управления!"])

    except Publication.DoesNotExist:
        return get_error_page(request, ["This is publication not found!", "Page not found: publ_manager/" + str(id) + "/"])