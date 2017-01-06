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
    url(r'^tree_manager/del_elem_in_tree/$', views.del_elem_in_tree, name='del_elem_in_tree'),
    url(r'^tree_manager/check_folder_for_delete/$', views.check_folder_for_delete, name='check_folder_for_delete'),
    url(r'^tree_manager/rename_publ_in_tree/$', views.rename_publ_in_tree, name='rename_publ_in_tree'),
    url(r'^tree_manager/rename_folder_in_tree/$', views.rename_folder_in_tree, name='rename_folder_in_tree'),
    url(r'^tree_manager/set_preview_publ_in_tree/$', views.set_preview_publ_in_tree, name='set_preview_publ_in_tree'),
    url(r'^tree_manager/remove_saved/$', views.remove_saved, name='remove_saved'),
    url(r'^tree_manager/get_path_to_folder/$', views.get_path_to_folder, name='get_path_to_folder_move'),
    url(r'^tree_manager/move_publication/$', views.move_publication, name='move_publication'),

    # События на странице управления конспектом
    url(r'^publ_manager/delete_publ_in_tree/$', views.delete_publ_in_tree, name='delete_publ_in_tree'),
    url(r'^publ_manager/(?P<id>[0-9]+)/save_main_publ_manager/$', views.save_main_publ_manager, name='save_main_publ_manager'),
    url(r'^publ_manager/(?P<id>[0-9]+)/save_opt_publ_manager/$', views.save_opt_publ_manager, name='save_opt_publ_manager'),
    url(r'^publ_manager/(?P<id>[0-9]+)/add_white_user/$', views.add_white_user, name='add_white_user'),
    url(r'^publ_manager/(?P<id>[0-9]+)/del_white_user/$', views.del_white_user, name='del_white_user'),
    url(r'^publ_manager/(?P<id>[0-9]+)/add_black_user/$', views.add_black_user, name='add_black_user'),
    url(r'^publ_manager/(?P<id>[0-9]+)/del_black_user/$', views.del_black_user, name='del_black_user'),

    # События на странице конспекта
    url(r'^page/(?P<id>[0-9]+)/add_dynamic_comment/$', views.add_dynamic_comment, name='add_dynamic_comment'),
    url(r'^page/(?P<id>[0-9]+)/reply_dynamic_comment/$', views.reply_dynamic_comment, name='reply_dynamic_comment'),
    url(r'^page/(?P<id>[0-9]+)/add_main_comment/$', views.add_main_comment, name='add_main_comment'),
    url(r'^page/(?P<id>[0-9]+)/save_publication/$', views.save_publication, name='save_publication'),
    url(r'^page/(?P<id>[0-9]+)/get_version/$', views.get_version, name='get_version'),
    url(r'^page/(?P<id>[0-9]+)/set_head/$', views.set_head, name='set_head'),
    url(r'^page/(?P<id>[0-9]+)/presentation/$', views.presentation, name='presentation'),
    url(r'^page/(?P<id>[0-9]+)/save_page/$', views.save_page, name='save_page'),
    url(r'^page/(?P<id>[0-9]+)/add_star_publication/$', views.add_star_publication, name='add_star_publication'),
    url(r'^page/(?P<id>[0-9]+)/load_md/$', views.load_md, name='load_md'),
    url(r'^page/(?P<id>[0-9]+)/get_path_to_folder/$', views.get_path_to_folder_id, name='get_path_to_folder_save'),

    # События на странице пользователя
    url(r'^user/(?P<id>[0-9]+)/send_request_colleagues/$', views.send_request_colleagues, name='send_request_colleagues'),

    # Событие, если сайт находится на ремонте
    url(r'^login_developer/$', views.login_developer, name='login_developer'),

    # События на странице коллег
    url(r'^colleagues/delete_colleague/$', views.delete_colleague, name='delete_colleague'),


    # Событие на странице уведомлений
    url(r'^notifications/add_colleague/(?P<id>[0-9]+)$', views.add_colleague, name='add_colleague'),
    url(r'^notifications/notification_read/$', views.notification_read, name='notification_read'),
    url(r'^notifications/delete_notification/$', views.delete_notification, name='delete_notification'),

    # События на странице настроек пользователя
    url(r'^settings/check_password/$', views.check_password, name='check_password'),
    url(r'^settings/check_nickname/$', views.check_nickname, name='check_nickname'),
    url(r'^settings/repassword_user/$', views.repassword_user, name='repassword_user'),
    url(r'^settings/renickname_user/$', views.renickname_user, name='renickname_user'),

    # События на странице создания конспекта
    url(r'^create/get_path_to_folder/$', views.get_path_to_folder, name='get_path_to_folder'),


]
