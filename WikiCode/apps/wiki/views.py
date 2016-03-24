from django.shortcuts import render
from .models import Publication, Statistics
from django.template import RequestContext, loader
from django.http import HttpResponse
from .mymarkdown import mdsplit


def index(request):
    all_publications = Publication.objects.all()
    context = {
        "all_publications": all_publications,
    }
    return render(request, 'wiki/index.html', context)


def about(request):
    context = {

    }
    return render(request, 'wiki/about.html', context)


def create(request):
    context = {

    }
    return render(request, 'wiki/create.html', context)


def edit(request):
    context = {

    }
    return render(request, 'wiki/edit.html', context)


def help(request):
    context = {

    }
    return render(request, 'wiki/help.html', context)


def page(request, id):
    publication = Publication.objects.get(id_publication=id)
    # Разбиваем весь текст на абзацы
    md_text = publication.text
    arr = mdsplit.mdSplit(md_text)
    print(arr)
    numbers = []
    paragraphs = []
    for i in range(0,len(arr)):
        numbers.append(str(i+1))
        paragraphs.append({
            "index": str(i+1),
            "text": arr[i]
        })

    context = {
        "publication": publication,
        "paragraphs":paragraphs,
        "numbers":numbers,

    }
    return render(request, 'wiki/page.html', context)


def settings(request):
    context = {

    }
    return render(request, 'wiki/settings.html', context)


def user(request):
    context = {

    }
    return render(request, 'wiki/user.html', context)


def registration(request):
    context = {

    }
    return render(request, 'wiki/registration.html', context)


def create_page(request):
    # Получаем данные формы
    form = request.POST
    # Проверяем, чего хотим сделать
    if request.POST.get('secret') == "off":
        with open("WikiCode/apps/wiki/generate_pages/gen_page.gen", "r", encoding='utf-8') as f:
            gen_page = f.read()
        first_part = '<!DOCTYPE html><html><title>' + form["title"] + '</title><xmp theme="' + form[
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
            id_author=0,
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
            tree_path="",
            comments=0,
            imports=0,
            marks=0,
            likes=0,
            read=0,
            edits=0)
        new_publication.save()
        all_publications = Publication.objects.all()
        context = {
            "all_publications": all_publications,
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


def test(request):
    text = """# Урок по языку Java!
Java - великолепный язык для кроссплатформенной разработки!
Вот пример кода на этом языке:
```
System.out.println("Hello world!");
```
Учите этот классный язык!
"""
    arr = mdsplit.mdSplit(text);
    print(arr)
    numbers = [];
    for i in range(0,len(arr)):
        numbers.append(str(i+1))

    paragraphs = []
    for i in range(0,len(arr)):
        paragraphs.append({
            "index": str(i+1),
            "text": arr[i]
        })
    context = {
        "paragraphs": paragraphs,
        "numbers":numbers,
    }
    return render(request, 'wiki/test.html', context)


def testform(request):
    form = request.POST
    print(form['md-elem-1'])
    context = {

    }
    return render(request, 'wiki/index.html', context)

def tree_manager(request):
    context = {

    }
    return render(request, 'wiki/tree_manager.html', context)
