# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render

from .auth import check_auth
from WikiCode.apps.wiki.models import User
from WikiCode.apps.wiki.my_libs.trees_management.manager import WikiTree


def get_tree_manager(request):

    user_data = check_auth(request)
    try:
        user = User.objects.get(email=user_data)
        wt = WikiTree(0)
        wt.load_tree(user.tree)

        context = {
            "user_data": user_data,
            "preview_tree": wt.generate_html_preview(),
            "dynamic_tree": wt.generate_html_dynamic(),
        }

        return render(request, 'wiki/tree_manager.html', context)
    except User.DoesNotExist:
        context = {
            "user_data": user_data,
        }
        return render(request, 'wiki/tree_manager.html', context)


def get_add_folder_in_tree(request):
    """Ajax представление. Добавление папки в дерево пользователя"""

    if request.method == "GET":
        answer = request.GET.get('answer')
        user_data = check_auth(request)
        split_answer = answer.split("^^^")
        folder_name = split_answer[0]
        path = split_answer[1].split(":")[0]

        try:
            user = User.objects.get(email=user_data)
            wt = WikiTree(0)
            wt.load_tree(user.tree)
            wt.add_folder(path,folder_name)
            user.tree = wt.get_tree()
            user.save()

            return HttpResponse('ok', content_type='text/html')

        except User.DoesNotExist:
            context = {
                "user_data": user_data,
            }
            return render(request, 'wiki/tree_manager.html', context)

    else:
        return HttpResponse('no', content_type='text/html')
