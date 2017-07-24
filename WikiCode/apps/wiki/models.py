#   # -*- coding: utf-8 -*-
#
#   Copyright (C) 2016-2017 Igor Soloduev <diahorver@gmail.com>
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

from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    user = models.OneToOneField(DjangoUser)
    id_user = models.BigIntegerField()
    nickname = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100)
    file_tree = models.TextField()
    preview_publ_id = models.BigIntegerField()

    def __str__(self):
        return str(self.id_user)


class Publication(models.Model):
    id_publication = models.BigIntegerField()
    id_author = models.BigIntegerField()
    nickname_author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    text = models.TextField()
    theme = models.CharField(max_length=50)
    tree_path = models.TextField()
    read = models.BigIntegerField()
    saves = models.BigIntegerField()
    # Все настройки конспекта
    is_public = models.BooleanField()
    is_dynamic_paragraphs = models.BooleanField()
    is_show_author = models.BooleanField()
    is_loading = models.BooleanField()
    is_saving = models.BooleanField()
    is_file_tree = models.BooleanField()

    def __str__(self):
        return str(self.id_publication)


# Модель папки
class Folder(models.Model):
    id_folder = models.BigIntegerField()
    id_author = models.BigIntegerField()
    date = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id_folder)


# Модель в единственном экземпляре, для хранения статистики
class Statistics(models.Model):
    id_statistics = models.IntegerField()
    # Зарегестрировано юзеров
    users_reg = models.BigIntegerField()
    # Зарегестрировано юзеров за всю историю
    users_total_reg = models.BigIntegerField(default=0)
    publications_create = models.BigIntegerField()
    total_folders = models.BigIntegerField()    # Всего создано папок

    def __str__(self):
        return str(self.id_statistics)


class Developer(models.Model):
    id_developer = models.IntegerField()
    name_developer = models.TextField(max_length=100)

    def __str__(self):
        return str(self.name_developer)


class InviteKeys(models.Model):
    key = models.CharField(max_length=16)

    def __str__(self):
        return str(self.id)