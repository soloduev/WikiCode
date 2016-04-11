# -*- coding: utf-8 -*-

from .auth import check_auth, get_user_id
from django.shortcuts import render
from WikiCode.apps.wiki.models import User as WikiUser
from django.contrib.auth.models import User as DjangoUser
from WikiCode.apps.wiki.models import Statistics
from WikiCode.apps.wiki.models import Publication
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from WikiCode.apps.wiki.my_libs.trees_management.manager import WikiTree
from WikiCode.apps.wiki.models import User


def get_user(request, id):

    user_data = check_auth(request)
    try:
        user = User.objects.get(email=user_data)
        if user.id_user == id:
            wt = WikiTree(user.id_user)
            wt.load_tree(user.tree)

            context = {
                "user_data": user_data,
                "user_id": get_user_id(request),
                "preview_tree": wt.generate_html_preview(),
                "user":user,
            }

            return render(request, 'wiki/user.html', context)
        else:
            other_user = User.objects.get(id_user=id)
            wt = WikiTree(other_user.id_user)
            wt.load_tree(other_user.tree)

            context = {
                "user_data": user_data,
                "user_id": get_user_id(request),
                "preview_tree": wt.generate_html_preview(),
                "user":other_user,
            }

            return render(request, 'wiki/user.html', context)

    except User.DoesNotExist:
        context = {
            "user_data": user_data,
            "user_id": get_user_id(request),
        }
        return render(request, 'wiki/user.html', context)


def get_create_user(request):
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

            # Создаем дерево по умолчанию для юзера
            new_tree = WikiTree(total_reg_users)

            # Создаем нового юзера
            new_wiki_user = WikiUser(user=user,
                                     nickname=form["user_nickname"],
                                     email=form["user_email"],
                                     id_user=total_reg_users,
                                     tree=new_tree.get_tree(),
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

            context = {
                "all_publications": all_publications,
                "user_data": check_auth(request),
            }
            return render(request, 'wiki/index.html', context)
        context = {
            "error": "Пользователь с таким Email уже существует",
            "user_data": check_auth(request),
            "user_id": get_user_id(request),
        }
        return render(request, 'wiki/registration.html', context)
    context = {
        "error": "Пользователь с таким Nickname уже существует",
        "user_data": check_auth(request),
        "user_id": get_user_id(request),
    }
    return render(request, 'wiki/registration.html', context)


def get_login_user(request):

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

    context = {
        "all_publications": all_publications,
        "user_data": check_auth(request),
        "user_id": get_user_id(request),
    }

    return render(request, 'wiki/index.html', context)


def get_logout_user(request):

    logout(request)
    all_publications = Publication.objects.all()

    context = {
        "all_publications": all_publications,
        "user_data": check_auth(request),
        "user_id": get_user_id(request),
    }

    return render(request, 'wiki/index.html', context)