# -*- coding: utf-8 -*-
from django.shortcuts import render
from WikiCode.apps.wiki.models import Publication, Statistics
from .auth import check_auth, get_user_id
from WikiCode.apps.wiki.mymarkdown import mdsplit
from django.template import RequestContext, loader
from django.http import HttpResponse
from WikiCode.apps.wiki.models import User
from WikiCode.apps.wiki.my_libs.trees_management.manager import WikiTree
from WikiCode.apps.wiki.my_libs.views_manager.error_view import get_error_page

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


def get_edit(request):
    context = {

    }

    return render(request, 'wiki/edit.html', context)


def get_page(request, id):
    try:
        publication = Publication.objects.get(id_publication=id)
        # Разбиваем весь текст на абзацы
        md_text = publication.text
        arr = mdsplit.mdSplit(md_text)
        print(arr)
        numbers = []
        paragraphs = []
        for i in range(0, len(arr)):
            numbers.append(str(i + 1))
            paragraphs.append({
                "index": str(i + 1),
                "text": arr[i]
            })

        context = {
            "publication": publication,
            "paragraphs": paragraphs,
            "numbers": numbers,
            "user_data": check_auth(request),
            "user_id": get_user_id(request),
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
            tree_path=form["folder"]+":"+str(newid),
            comments=0,
            imports=0,
            marks=0,
            likes=0,
            read=0,
            edits=0)
        new_publication.save()

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
