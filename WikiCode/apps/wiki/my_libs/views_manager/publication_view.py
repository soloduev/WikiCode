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


from django.shortcuts import render
from WikiCode.apps.wiki.models import Publication, Statistics, CommentBlock, Comment, Paragraphs, DynamicCommentParagraph, DynamicComment, Like, \
    Viewing
from .auth import check_auth, get_user_id
from WikiCode.apps.wiki.my_libs.WikiMarkdown import WikiMarkdown
from django.template import RequestContext, loader
from django.http import HttpResponse
from WikiCode.apps.wiki.models import User
from WikiCode.apps.wiki.my_libs.trees_management.manager import WikiTree
from WikiCode.apps.wiki.my_libs.views_manager.error_view import get_error_page
import datetime

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

        context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
            "dynamic_tree": wt.generate_html_dynamic_folders(),
            "path": path,
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

        # Теперь загружаем комментарии

        try:
            comment_block = CommentBlock.objects.get(id_publication=id)
            all_comments = Comment.objects.filter(comment_block=comment_block)
        except CommentBlock.DoesNotExist:
            print("WIKI ERROR: Блок комментариев не обнаружен")
        except Comment.DoesNotExist:
            print("WIKI ERROR: Список комментариев не обнаружен")

        prgrphs = []

        # Теперь загружаем динамические комментарии
        try:
            db_paragraphs = Paragraphs.objects.get(id_publication=id)
            dynamic_comments_paragraphs = DynamicCommentParagraph.objects.filter(paragraphs=db_paragraphs)
            for elem in dynamic_comments_paragraphs:
                if elem.is_comment == True:
                    # Получаем все комментарии к этому блоку
                    dynamic_comments = DynamicComment.objects.filter(dynamic_comment_paragraph=elem)
                    block = {'num_pos': elem.num_position, 'comments': dynamic_comments}
                    prgrphs.append(block)

        except Paragraphs.DoesNotExist:
            print("WIKI ERROR: Paragraphs не обнаружен")
        except DynamicCommentParagraph.DoesNotExist:
            print("WIKI ERROR: DynamicCommentParagraph не обнаружен")
        except DynamicComment.DoesNotExist:
            print("WIKI ERROR: DynamicComment не обнаружен")

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
            "preview_tree": wt.generate_html_preview(),
            "all_comments": all_comments,
            "prgrphs": prgrphs,
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
        context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
        }
        print("ERROR!!!!--------------")
        return render(request, 'wiki/index.html', context)
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
        stat.save()

        name_page = str(num + 1)
        f = open("media/publications/" + name_page + ".html", 'tw', encoding='utf-8')
        f.close()

        with open("media/publications/" + name_page + ".html", "wb") as f:
            f.write(ready_page.encode("utf-8"))
        newid = num + 1
        new_publication = Publication(
            id_publication=newid,
            id_author=user.id_user,
            nickname_author=user.nickname,
            title=form["title"],
            description=form["description"],
            text=form["text"],
            theme=form["theme"],
            html_page="publications/" + name_page + ".html",
            is_private=False,
            is_public=False,
            is_private_edit=False,
            is_public_edit=False,
            is_marks=False,
            is_comments=False,
            tags=form["tags"],
            tree_path=form["folder"]+form["title"]+".publ:"+str(newid),
            comments=0,
            imports=0,
            marks=0,
            likes=0,
            read=0,
            edits=0,
            downloads=0)
        new_publication.save()

        # Создаем пустой общий блок комментирования
        new_comment_block = CommentBlock(
            id_publication=newid,
            last_id=0)
        new_comment_block.save()

        # Получаем количество параграфов
        wm = WikiMarkdown()
        size_paragraphs = len(wm.split(form["text"]))

        # Создаем пустые динамичные параграфы комментирования
        new_paragraphs = Paragraphs(
            id_publication=newid,
            last_id=size_paragraphs)
        new_paragraphs.save()

        # Соответственно создаем для каждого из них параграф
        # Данная операция, ну совсем уж не быстрая, если конспект достаточно большой
        for i in range(1, size_paragraphs):
            dynamic_comment_paragraph = DynamicCommentParagraph(
                paragraphs=new_paragraphs,
                num_position=i,
                is_comment=False)
            dynamic_comment_paragraph.save()


        # Загружаем дерево пользователя
        wt = WikiTree(user.id_user)
        wt.load_tree(user.tree)
        # Добавляем этот конспект в папку
        wt.add_publication(form["folder"],form["title"],newid)
        user.tree = wt.get_tree()
        # Увеличиваем количество публикаций в статистике у пользователя
        user.publications += 1
        user.save()

        all_publications = Publication.objects.all()

        context = {
            "all_publications": all_publications,
            "user_data": user_data,
            "user_id": get_user_id(request),
        }
        return render(request, 'wiki/index.html', context)
    else:
        first_part = '<!DOCTYPE html><html><title>' + form["title"] + '</title><xmp theme="' + form[
            "theme"].lower() + '" style="display:none;">'
        second_part = form["text"]
        third_part = '</xmp><script src="http://strapdownjs.com/v/0.2/strapdown.js"></script></html>'
        total = first_part + second_part + third_part
        with open("WikiCode/apps/wiki/templates/preview.html", "wb") as f:
            f.write(total.encode("utf-8"))
        template = loader.get_template('preview.html')
        context = RequestContext(request, {

        })
        return HttpResponse(template.render(context))


def get_publ_manager(request, id):
    """Запускает страницу управления конспектом"""

    try:
        # Получаем пользователя
        user_data = check_auth(request)

        # Получаем конспект, который хотим управлять
        publication = Publication.objects.get(id_publication=id)

        # Проверяем, является ли автором этого конспекта тот пользователь
        # Который захотел управлять этим конспектом
        current_id = get_user_id(request)
        if current_id == publication.id_author:

            context = {
                "user_data": user_data,
                "user_id": current_id,
                "publication":publication,
                "tree_path":publication.tree_path.split(":")[0],
            }
            return render(request, 'wiki/publ_manager.html', context)
        else:
            return get_error_page(request, ["У Вас нет доступа к этому конспекту, чтобы управлять им!", "Вы не являетесь редактором конспекта page/" + str(id) + "/"])

    except Publication.DoesNotExist:
        return get_error_page(request, ["This is publication not found!", "Page not found: publ_manager/" + str(id) + "/"])


def get_add_comment_in_wiki_page(request, id):
    """Ajax представление. Добавляет коммент к публикации."""

    try:
        comment_block = CommentBlock.objects.get(id_publication=id)
        publication = Publication.objects.get(id_publication=id)

        # Получаем пользователя
        user_data = check_auth(request)

        # Получаем сообщение
        comment_message = request.GET.get('comment_message')

        #Получаем текущую дату
        date = str(datetime.datetime.now())
        date = date[:len(date)-7]

        #Получаем пользователя оставившего комментарий
        id = int(get_user_id(request))
        user = User.objects.get(id_user=id)
        user.comments += 1

        #Получаем пользователя получившего комментарий
        user2 = User.objects.get(id_user=publication.id_author)
        user2.commented_it += 1


        # Создаем новый комментарий
        new_comment = Comment(comment_block=comment_block,
                              num_position=comment_block.last_id+1,
                              id_author=user.id_user,
                              nickname_author=user.nickname,
                              rating=0,
                              text=comment_message,
                              data=date,
                              id_author_answer=0,
                              nickname_author_answer="")

        new_comment.save()
        comment_block.last_id += 1
        comment_block.save()
        user2.save()
        user.save()

        return HttpResponse('ok', content_type='text/html')

    except CommentBlock.DoesNotExist:
        return get_error_page(request, ["This is comment block not found!"])
    except Publication.DoesNotExist:
        return get_error_page(request, ["This is publication not found!"])
    except User.DoesNotExist:
        return get_error_page(request, ["This is user is not found!"])



def get_add_dynamic_comment_in_wiki_page(request, id):
    """Ajax представление. Добавляет динамический комментарий к азбзацу публикации."""

    try:
        paragraphs = Paragraphs.objects.get(id_publication=id)
        publication = Publication.objects.get(id_publication=id)

        # Получаем пользователя
        user_data = check_auth(request)

        # Получаем сообщение
        comment_message = request.GET.get('comment_message')
        # Получаем номер параграфа в данной публикации
        num_paragraph = request.GET.get('num_paragraph')
        print(comment_message)
        print(num_paragraph)
        # Получаем текущую дату
        date = str(datetime.datetime.now())
        date = date[:len(date) - 7]

        # Получаем пользователя оставившего комментарий
        id = int(get_user_id(request))
        user = User.objects.get(id_user=id)
        user.comments += 1


        # Получаем тот параграф, в который мы хотим добавить комментарий
        dynamic_comment_paragraph =  DynamicCommentParagraph.objects.get(num_position=int(num_paragraph))

        # Создаем новый динамический комментарий

        new_dynamic_comment = DynamicComment(
            dynamic_comment_paragraph=dynamic_comment_paragraph,
            num_position=dynamic_comment_paragraph.last_id + 1,
            id_author=user.id_user,
            nickname_author=user.nickname,
            text=comment_message,
            data=date)

        new_dynamic_comment.save()
        dynamic_comment_paragraph.last_id += 1
        dynamic_comment_paragraph.is_comment = True
        dynamic_comment_paragraph.save()
        user.save()

        return HttpResponse('ok', content_type='text/html')

    except Paragraphs.DoesNotExist:
        return get_error_page(request, ["This is paragraphs not found!"])
    except Publication.DoesNotExist:
        return get_error_page(request, ["This is publication not found!"])
    except User.DoesNotExist:
        return get_error_page(request, ["This is user is not found!"])
    except DynamicCommentParagraph.DoesNotExist:
        return get_error_page(request, ["This is DynamicCommentParagraph is not found!"])


def get_like_wiki_page(request, id):
    """Ajax представление. Добавляет или убирает like с публикации"""
    try:
        # Получаем пользователя захотевшего поставить лайк
        id_user = int(get_user_id(request))

        if id_user==-1:
            return HttpResponse('no', content_type='text/html')
        else:
            # Получаем текущую дату
            date = str(datetime.datetime.now())
            date = date[:len(date) - 7]

            # Получаем User
            user = User.objects.get(id_user=id_user)
            # Получаем публикацию на которой произошел лайк
            publication = Publication.objects.get(id_publication=id)

            # Проверяем, не стоит ли like уже у этого пользователя на этот конспект
            is_set = False
            try:
                like = Like.objects.get(id_user=id_user, id_publ_like=id)
                # Лайк стоит, убираем
                like.delete()
                publication.likes-=1
                publication.save()
            except Like.DoesNotExist:
                # Лайк не стоит. Ставим
                new_like = Like(id_user=id_user,
                                nickname=user.nickname,
                                type="publ",
                                id_publ_like=id,
                                id_user_like=-1,
                                date=date)
                new_like.save()
                publication.likes+=1
                publication.save()


            return HttpResponse('ok', content_type='text/html')
    except User.DoesNotExist:
        return get_error_page(request, ["This is user is not found!"])
    except Publication.DoesNotExist:
        return get_error_page(request, ["This is Publication is not found!"])