from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^create/$', views.create, name='create'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^help/$', views.help, name='help'),
    url(r'^page/(?P<id>[0-9]+)/$', views.page, name='page'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^user/(?P<id>[0-9]+)/$', views.user, name='user'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^tree_manager/$',views.tree_manager, name='tree_manager'),


    url(r'^create_page/$', views.create_page, name='create_page'),
    url(r'^create_user/$', views.create_user, name='create_user'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    url(r'^registration/check_nickname/$', views.check_nickname, name='check_nickname'),
    url(r'^registration/check_email/$', views.check_email, name='check_email'),

    # События в менеджере дерева
    url(r'^tree_manager/add_folder_in_tree/$', views.add_folder_in_tree, name='add_folder_in_tree'),
    url(r'^tree_manager/del_elem_in_tree/$', views.del_elem_in_tree, name='del_elem_in_tree'),

]
