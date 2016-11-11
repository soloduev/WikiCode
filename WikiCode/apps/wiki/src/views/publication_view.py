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


import datetime, json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from WikiCode.apps.wiki.models import Publication, Statistics, Viewing, DynamicComment, Comment
from WikiCode.apps.wiki.models import User
from WikiCode.apps.wiki.settings import wiki_settings
from WikiCode.apps.wiki.src.modules.wiki_comments.wiki_comments import WikiComments
from WikiCode.apps.wiki.src.modules.wiki_tree.wiki_tree import WikiFileTree
from WikiCode.apps.wiki.src.modules.wiki_versions.wiki_versions import WikiVersions
from WikiCode.apps.wiki.src.views.error_view import get_error_page
from WikiCode.apps.wiki.src.wiki_markdown import WikiMarkdown
from .auth import check_auth, get_user_id


def get_create(request):
    user_data = check_auth(request)
    try:
        # Получения id папки, в которой хотим создать конспект
        input_folder_id = ""
        full_path = str(request.POST.get('folder_publ'))

        if full_path != "None" and full_path != "NONE":
            input_folder_id = full_path
        user = User.objects.get(email=user_data)

        wft = WikiFileTree()
        wft.load_tree(user.file_tree)

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
            wft = WikiFileTree()
            wft.load_tree(user.file_tree)
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

            wft = WikiFileTree()
            wft.load_tree(author_user.file_tree)
            html_preview_tree = wft.to_html_preview()
        except User.DoesNotExist:
            print("Автора не существует")

        # Загружаем все динамические комментарии в этой публикации
        if wiki_settings.MODULE_DYNAMIC_PARAGRAPHS:
            arr_dynamic_comments = DynamicComment.objects.filter(publication=publication)
            dynamic_comments = []
            # Далее, к составляем расширенный массив, с именем автора
            for comment in arr_dynamic_comments:
                try:
                    name_author = User.objects.get(id_user=comment.id_author)
                    name_author = name_author.nickname
                except User.DoesNotExist:
                    name_author = "Undefined"
                dynamic_comments.append({
                    "publication": comment.publication,
                    "paragraph": comment.paragraph,
                    "position": comment.position,
                    "id_author": comment.id_author,
                    "text": comment.text,
                    "rating": comment.rating,
                    "date": comment.date,
                    "name_author": name_author
                })


        else:
            dynamic_comments = None

        if wiki_settings.MODULE_VERSIONS:
            wiki_version = WikiVersions()
            wiki_version.load_versions(publication.versions)
            versions_js = wiki_version.generate_js()
        else:
            versions_js = None

        # Конвертируем общие комментарии
        wiki_comments = WikiComments()
        wiki_comments.load_comments(publication.main_comments)

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
            "module_dynamic_paragraphs": wiki_settings.MODULE_DYNAMIC_PARAGRAPHS,
            "dynamic_comments": dynamic_comments,
            "module_main_comments": wiki_settings.MODULE_MAIN_COMMENTS,
            "main_comments": wiki_comments.to_html(),
            "main_comments_count": wiki_comments.get_count(),
            "module_versions": wiki_settings.MODULE_VERSIONS,
            "versions_js": versions_js
        }

        return render(request, 'wiki/page/page.html', context)
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
            # Создаем первые комментарии
            wiki_comments = WikiComments()
            wiki_comments.create_comments(newid)

            # Создаем первую версию конспекта
            wiki_versions = WikiVersions()
            wm = WikiMarkdown()                 # Получаем все абзацы
            paragraphs = wm.split(form["text"])
            wiki_versions.create_versions(id_user=user.id_user,
                                          seq=list(paragraphs))
            archive = wiki_versions.get_archive()

            new_publication = Publication(
                id_publication=newid,
                id_author=user.id_user,
                nickname_author=user.nickname,
                title=form["title"],
                description=form["description"],
                text=form["text"],
                theme=form["theme"],
                html_page=ready_page,
                tree_path=form["folder"],
                read=0,
                main_comments=wiki_comments.get_xml_str(),
                versions=archive)

        # Загружаем дерево пользователя
        wft = WikiFileTree()
        wft.load_tree(user.file_tree)

        # Добавляем этот конспект в папку
        wft.create_publication(id=newid,
                               name=form["title"],
                               access="public",
                               type="personal",
                               id_folder=form['folder'].split(':')[1])  # new version

        user.file_tree = wft.get_xml_str()                              # new version

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
                "tree_path":_publication.tree_path
            }
            return render(request, 'wiki/publ_manager.html', context)
        else:
            return get_error_page(request, ["Вы не являетесь автором данного конспекта, чтобы перейти в панель управления!"])

    except Publication.DoesNotExist:
        return get_error_page(request, ["This is publication not found!", "Page not found: publ_manager/" + str(id) + "/"])


@csrf_protect
def get_add_dynamic_comment(request, id):
    """Ajax представление. Добавление комментария."""

    if request.method == "POST":
        # Проверяем, аутентифицирован ли пользователь
        if get_user_id(request) == -1:
            return HttpResponse('no', content_type='text/html')
        else:
            # Если пользователь аутентифицирован то, добавляем динамический комментарий к теущему конспекту

            try:
                # Получаем текущую публикацию
                publication = Publication.objects.get(id_publication=id)

                # Получаем комментарий, который хотим оставить
                dynamic_comment = request.POST.get('dynamic_comment')

                # Получаем номер абзаца, в котором оставил пользователь комментарий
                num_paragraph = request.POST.get('num_paragraph')

                # Получаем все комментарии данного параграфа
                dynamic_comments = DynamicComment.objects.filter(publication=publication, paragraph=num_paragraph)

                # Получаем текущую дату
                date = str(datetime.datetime.now())
                date = date[:len(date) - 7]

                # Получаем текущую позицию комментария в текущем абзаце
                if not dynamic_comments:
                    position = 0
                else:
                    position = dynamic_comments[len(dynamic_comments)-1].position + 1

                # Создаем динамический комментарий
                new_dynamic_comment = DynamicComment(publication=publication,
                                                     paragraph=num_paragraph,
                                                     position=position,
                                                     id_author=get_user_id(request),
                                                     text=dynamic_comment,
                                                     rating=0,
                                                     date=date)

                new_dynamic_comment.save()

                return HttpResponse('ok', content_type='text/html')

            except Publication.DoesNotExist:
                return get_error_page(request, ["This is publication not found!",
                                                "Page not found: publ_manager/" + str(id) + "/"])
    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_add_main_comment(request, id):
    """Ajax представление. Добавление общего комментария."""

    if request.method == "POST":
        # Проверяем, аутентифицирован ли пользователь
        if get_user_id(request) == -1:
            return HttpResponse('no', content_type='text/html')
        else:
            # Если пользователь аутентифицирован то, добавляем общий комментарий к текущему конспекту

            try:
                # Получаем текущую публикацию
                publication = Publication.objects.get(id_publication=id)

                # Получаем пользователя, оставляющего комментарий
                current_user = User.objects.get(id_user=get_user_id(request))

                # Получаем комментарий, который хотим оставить
                main_comment = request.POST.get('main_comment')

                # Получаем id автора, которому нужно ответить
                reply_id = int(request.POST.get('reply_author_id'))

                # Загружаем имеющиеся комментарии у конспекта
                wiki_comments = WikiComments()
                wiki_comments.load_comments(publication.main_comments)

                # Узнаем количество комментариев
                stat = Statistics.objects.get(id_statistics=1)
                total_comments = stat.total_comments

                # Если комментарий не пустой
                if main_comment:

                    # Получаем текущую дату
                    date = str(datetime.datetime.now())
                    date = date[:len(date) - 7]

                    new_comment = Comment(id_comment=total_comments + 1,
                                          id_author=get_user_id(request),
                                          text=main_comment,
                                          id_publication=id,
                                          date=date)

                    # Повышаем у статистики количество созданных комментариев
                    stat.total_comments += 1

                    # Если пользователь создал новый комментарий, ни кому не ответив:
                    if reply_id == -1:
                        # Создаем новый комментарий в xml
                        wiki_comments.create_comment(id_comment=total_comments + 1,
                                                     user_id=get_user_id(request),
                                                     text=main_comment,
                                                     user_name=current_user.nickname,
                                                     date=date,
                                                     is_moderator=False)
                    else:
                        # Отвечаем на существующий комментарий
                        wiki_comments.reply(new_id=total_comments + 1,
                                            user_id=get_user_id(request),
                                            user_name=current_user.nickname,
                                            text=main_comment,
                                            reply_id=reply_id,
                                            date=date,
                                            is_moderator=False)

                    # Обновляем все комментарии в публикации
                    publication.main_comments = wiki_comments.get_xml_str()

                    # Сохраняем все изменения в БД
                    publication.save()
                    stat.save()
                    new_comment.save()

                    return HttpResponse('ok', content_type='text/html')
                else:
                    print("Пустой комментарий добавлять нельзя!")
                    return HttpResponse('no', content_type='text/html')

            except Publication.DoesNotExist:
                return get_error_page(request, ["This is publication not found!",
                                                "Page not found: publ_manager/" + str(id) + "/"])
            except User.DoesNotExist:
                return get_error_page(request, ["This is user not found!",
                                    "User not found: user/" + str(get_user_id(request)) + "/"])
    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_save_publication(request, id):
    """Ajax представление. Сохранение изменений в конспекте."""

    # Вспомогательный метод. Создает новую версию
    def create_new_version(md_paragraphs, publication):
        wiki_versions = WikiVersions()
        wiki_versions.load_versions(publication.versions)
        wiki_versions.new_version(publication.id_author, md_paragraphs)
        wiki_versions.set_head(wiki_versions.get_count_versions())
        new_text = ""
        for p in wiki_versions.get_head():
            new_text += p
        publication.text = new_text
        publication.versions = wiki_versions.get_archive()
        publication.save()

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
                    md_text += request.POST.get(str(i+1))
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
                        # Если версии не равны, порождаем новую.
                        create_new_version(md_paragraphs, publication)
                        return HttpResponse('not_eq', content_type='text/html')
                else:
                    # Порождаем новую версию
                    create_new_version(md_paragraphs, publication)
                    return HttpResponse('not_eq', content_type='text/html')

            except Publication.DoesNotExist:
                return get_error_page(request, ["This is publication not found!",
                                                "Page not found: publ_manager/" + str(id) + "/"])
    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_get_version(request, id):
    """ Ajax представление. Получение конкретной версии конспекта """

    if request.method == "GET":
        # Если пользователь аутентифицирован то, начинаем получать все изменения
        try:
            # Получаем текущую публикацию
            publication = Publication.objects.get(id_publication=id)
            # Получаем версию, которую нужно отобразить
            to_version = int(request.GET.get("to_version"))

            wiki_versions = WikiVersions()
            wiki_versions.load_versions(publication.versions)
            paragraphs = wiki_versions.get_version(to_version)

            context = {}

            for i in range(0, len(paragraphs)):
                context[str(i+1)] = paragraphs[i]

            context["count"] = str(len(paragraphs))

            return HttpResponse(json.dumps(context), content_type="application/json")

        except Publication.DoesNotExist:
            return get_error_page(request, ["This is publication not found!",
                                            "Page not found: publ_manager/" + str(id) + "/"])
    else:
        return HttpResponse('no', content_type='text/html')


@csrf_protect
def get_set_head(request, id):
    """ Ajax представление. становление выбранной версии как HEAD """

    if request.method == "POST":
        # Проверяем, аутентифицирован ли пользователь
        if get_user_id(request) == -1:
            return HttpResponse('auth', content_type='text/html')
        else:
            # Если пользователь аутентифицирован то, начинаем получать все изменения
            try:
                # Получаем текущую публикацию
                publication = Publication.objects.get(id_publication=id)
                # Получаем пользователя, оставляющего комментарий
                current_user = User.objects.get(id_user=get_user_id(request))
                # Получаем версию, которую необходимо сделать HEAD
                to_version = int(request.POST.get("to_version"))
                # Переключаем версию
                wiki_markdown = WikiMarkdown()
                wiki_versions = WikiVersions()
                wiki_versions.load_versions(publication.versions)
                wiki_versions.set_head(to_version)
                # Устанавливаем новое состояние версий
                publication.versions = wiki_versions.get_archive()
                # Получаем чисто текст текущей
                paragraphs = wiki_versions.get_head()
                md_text = ""
                for paragraph in paragraphs:
                    md_text += paragraph
                # Устанавливаем текущий текст конспекта
                publication.text = md_text
                # Сохраняем все изменения в БД
                publication.save()

                return HttpResponse('ok', content_type='text/html')
            except Publication.DoesNotExist:
                return get_error_page(request, ["This is publication not found!",
                                                "Page not found: publ_manager/" + str(id) + "/"])
    else:
        return HttpResponse('no', content_type='text/html')