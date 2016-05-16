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

from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^create/$', views.create, name='create'),
    url(r'^page/(?P<id>[0-9]+)/$', views.page, name='page'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^user/(?P<id>[0-9]+)/$', views.user, name='user'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^login/$', views.login, name='login'),
    url(r'^tree_manager/$',views.tree_manager, name='tree_manager'),
    url(r'^publ_manager/(?P<id>[0-9]+)$',views.publ_manager, name='publ_manager'),
    url(r'^colleagues/$',views.colleagues, name='colleagues'),
    url(r'^notifications/$',views.notifications, name='notifications'),
    url(r'^bug_report/$',views.bug_report, name='bug_report'),
    url(r'^bug_report/send_bug/$',views.send_bug, name='send_bug'),

    url(r'^create_page/$', views.create_page, name='create_page'),
    url(r'^create_user/$', views.create_user, name='create_user'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    url(r'^registration/check_nickname/$', views.check_nickname, name='check_nickname'),
    url(r'^registration/check_email/$', views.check_email, name='check_email'),

    # События в менеджере дерева
    url(r'^tree_manager/add_folder_in_tree/$', views.add_folder_in_tree, name='add_folder_in_tree'),
    url(r'^tree_manager/add_folder_in_saved_tree/$', views.add_folder_in_saved_tree, name='add_folder_in_saved_tree'),
    url(r'^tree_manager/del_elem_in_tree/$', views.del_elem_in_tree, name='del_elem_in_tree'),
    url(r'^tree_manager/del_elem_in_tree_saved/$', views.del_elem_in_tree_saved, name='del_elem_in_tree_saved'),
    url(r'^tree_manager/del_publ_in_tree_saved/$', views.del_publ_in_tree_saved, name='del_publ_in_tree_saved'),
    url(r'^tree_manager/check_folder_for_delete/$', views.check_folder_for_delete, name='check_folder_for_delete'),
    url(r'^tree_manager/check_folder_for_delete_saved/$', views.check_folder_for_delete_saved, name='check_folder_for_delete_saved'),
    url(r'^tree_manager/rename_publ_in_tree/$', views.rename_publ_in_tree, name='rename_publ_in_tree'),
    url(r'^tree_manager/rename_folder_in_tree/$', views.rename_folder_in_tree, name='rename_folder_in_tree'),
    url(r'^tree_manager/set_preview_publ_in_tree/$', views.set_preview_publ_in_tree, name='set_preview_publ_in_tree'),

    # События на странице управления конспектом
    url(r'^publ_manager/delete_publ_in_tree/$', views.delete_publ_in_tree, name='delete_publ_in_tree'),
    url(r'^publ_manager/(?P<id>[0-9]+)/save_access/$', views.save_access, name='save_access'),
    url(r'^publ_manager/check_nickname_for_add_editor/$', views.check_nickname_for_add_editor, name='check_nickname_for_add_editor'),
    url(r'^publ_manager/add_editor/$', views.add_editor, name='add_editor'),
    url(r'^publ_manager/remove_editor/$', views.remove_editor, name='remove_editor'),

    # События на странице конспекта
    url(r'^page/(?P<id>[0-9]+)/add_comment_in_wiki_page/$', views.add_comment_in_wiki_page, name='add_comment_in_wiki_page'),
    url(r'^page/(?P<id>[0-9]+)/add_dynamic_comment_in_wiki_page/$', views.add_dynamic_comment_in_wiki_page, name='add_dynamic_comment_in_wiki_page'),
    url(r'^page/(?P<id>[0-9]+)/like_wiki_page/$', views.like_wiki_page, name='like_wiki_page'),
    url(r'^page/(?P<id>[0-9]+)/import_wiki_page/$', views.import_wiki_page, name='import_wiki_page'),

    # События на странице пользователя
    url(r'^user/(?P<id>[0-9]+)/like_user/$', views.like_user, name='like_user'),

    # Событие, если сайт находится на ремонте
    url(r'^login_developer/$', views.login_developer, name='login_developer'),

    # События на странице коллег
    url(r'^colleagues/add_colleague/$', views.add_colleague, name='add_colleague'),
    url(r'^colleagues/remove_colleague/$', views.remove_colleague, name='remove_colleague'),


]
