from django.shortcuts import render

from WikiCode.apps.wiki.models import User as WikiUser
from .models import Publication, Statistics
from django.template import RequestContext, loader
from django.http import HttpResponse
from .mymarkdown import mdsplit
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def index(request):

    all_publications = Publication.objects.all()
    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    context = {
        "all_publications": all_publications,
        "user_data": user_data,
    }
    return render(request, 'wiki/index.html', context)


def about(request):

    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    context = {
        "user_data": user_data,
    }
    return render(request, 'wiki/about.html', context)


@login_required
def create(request):

    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    context = {
        "user_data": user_data,
    }
    return render(request, 'wiki/create.html', context)


@login_required
def edit(request):
    context = {

    }
    return render(request, 'wiki/edit.html', context)


def help(request):

    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    context = {
        "user_data" : user_data,
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

    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    context = {
        "publication": publication,
        "paragraphs":paragraphs,
        "numbers":numbers,
        "user_data":user_data,

    }
    return render(request, 'wiki/page.html', context)


@login_required
def settings(request):

    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    context = {
        "user_data":user_data,
    }
    return render(request, 'wiki/settings.html', context)


@login_required
def user(request):

    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    context = {
        "user_data":user_data,
    }
    return render(request, 'wiki/user.html', context)


def registration(request):

    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    context = {
        "user_data":user_data,
    }
    return render(request, 'wiki/registration.html', context)


def create_user(request):
    """Регистрация нового пользователя"""

    # Получаем данные формы
    form = request.POST

    # Проверяем на существование такого имени и email.
    # Осли проверка успешна, пользователя не создаем
    try:
            simple1 = WikiUser.objects.get(nickname=form["user_nickname"])
    except WikiUser.DoesNotExist:
        try:
            simple2 = WikiUser.objects.get(email=form["user_email"])
        except WikiUser.DoesNotExist:

            # Создаем нового пользователя
            user = DjangoUser.objects.create_user(form["user_nickname"],
                                                  form["user_email"],
                                                  form["user_password"])

            stat = Statistics.objects.get(id_statistics=1)
            # Необходимо для создания id пользователей
            total_reg_users = stat.users_total_reg
            stat.users_total_reg += 1
            stat.users_reg += 1
            stat.save()

            # Создаем нового юзера
            new_wiki_user = WikiUser(user=user,
                                     nickname=form["user_nickname"],
                                     email=form["user_email"],
                                     id_user=total_reg_users,
                                     avatar="none.jpg",
                                     name="anonymous",
                                     likes=0,
                                     publications=0,
                                     imports=0,
                                     comments=0,
                                     imports_it=0,
                                     commented_it=0)

            new_wiki_user.save()

            user = authenticate(username=form["user_nickname"], password=form["user_password"])

            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    print(">>>>>>>>>>>>>> WIKI ERROR: disabled account")
                    ...
            else:
                print(">>>>>>>>>>>>>> WIKI ERROR: invalid login")
                ...

            all_publications = Publication.objects.all()

            if request.user.is_authenticated():
                user_data = (request.user.email)
            else:
                user_data = ("None")

            context = {
                "all_publications": all_publications,
                "user_data": user_data,
            }
            return render(request, 'wiki/index.html', context)
        context = {
            "error": "Пользователь с таким Email уже существует"
        }
        return render(request, 'wiki/registration.html', context)
    context = {
        "error": "Пользователь с таким Nickname уже существует"
    }
    return render(request, 'wiki/registration.html', context)


def login_user(request):

    user_name = request.POST['user_name']
    user_password = request.POST['user_password']

    user = authenticate(username=user_name, password=user_password)

    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            print(">>>>>>>>>>>>>> WIKI ERROR: disabled account")
            ...
    else:
        print(">>>>>>>>>>>>>> WIKI ERROR: invalid login")
        ...

    all_publications = Publication.objects.all()

    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    context = {
        "all_publications": all_publications,
        "user_data": user_data,
    }
    return render(request, 'wiki/index.html', context)

@login_required
def logout_user(request):
    logout(request)
    all_publications = Publication.objects.all()

    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    context = {
        "all_publications": all_publications,
        "user_data": user_data,
    }
    return render(request, 'wiki/index.html', context)


@login_required
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

        if request.user.is_authenticated():
            user_data = (request.user.email)
        else:
            user_data = ("None")

        context = {
            "all_publications": all_publications,
            "user_data" : user_data,
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


@login_required
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


@login_required
def testform(request):
    form = request.POST
    print(form['md-elem-1'])
    context = {

    }
    return render(request, 'wiki/index.html', context)


@login_required
def tree_manager(request):

    if request.user.is_authenticated():
        user_data = (request.user.email)
    else:
        user_data = ("None")

    context = {
        "user_data": user_data,
    }
    return render(request, 'wiki/tree_manager.html', context)


def check_nickname(request):
    """Ajax представление. Проверка на существование такого nickname в базе данных"""

    if request.method == "GET":
        request.session['nickname'] = request.GET['nickname']
        nickname = request.GET['nickname']

        try:
            user = WikiUser.objects.get(nickname=nickname)
        except WikiUser.DoesNotExist:
            if nickname.lower() == "admin":
                return HttpResponse('ok', content_type='text/html')
            else:
                return HttpResponse('no', content_type='text/html')

        return HttpResponse('ok', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')


def check_email(request):
    """Ajax представление. Проверка на существование такого email в базе данных"""

    if request.method == "GET":
        request.session['email'] = request.GET['email']
        email = request.GET['email']

        try:
            user = WikiUser.objects.get(email=email)
        except WikiUser.DoesNotExist:
            if email == "diahorver@gmail.com":
                return HttpResponse('ok', content_type='text/html')
            else:
                return HttpResponse('no', content_type='text/html')

        return HttpResponse('ok', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')
