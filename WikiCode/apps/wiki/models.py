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

from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    user = models.OneToOneField(DjangoUser)
    id_user = models.BigIntegerField()
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    tree = models.TextField()
    publications = models.BigIntegerField()
    avatar = models.ImageField(upload_to='avatars')
    preview_publ_id = models.BigIntegerField()

    def __str__(self):
        return str(self.id_user)


class Publication(models.Model):
    id_publication = models.BigIntegerField()
    id_author = models.BigIntegerField()
    nickname_author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    text = models.TextField()
    theme = models.CharField(max_length=50)
    html_page = models.TextField()
    tree_path = models.TextField()
    read = models.BigIntegerField()

    def __str__(self):
        return str(self.id_publication)


# Модель отдельного динамического комментария
class DynamicComment(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    num_position = models.BigIntegerField()
    id_author = models.BigIntegerField()
    text = models.TextField()
    rating = models.BigIntegerField()
    date = models.CharField(max_length=100)

    def __str__(self):
            return str(str(self.publication) + "_" + str(self.num_position))


# Модель просмотра страницы. Указывает кто просмотрел и когда
class Viewing(models.Model):
    id_user = models.BigIntegerField()
    nickname = models.CharField(max_length=100)
    id_publ = models.BigIntegerField()
    date = models.CharField(max_length=100)

    def __str__(self):
        return str("user:" + str(self.id_user) +
                   " publ:" + str(self.id_publ))


class Statistics(models.Model):
    id_statistics = models.IntegerField()
    # Зарегестрировано юзеров
    users_reg = models.BigIntegerField()
    # Зарегестрировано юзеров за всю историю
    users_total_reg = models.BigIntegerField(default=0)
    user_online = models.BigIntegerField()
    publications_create = models.BigIntegerField()

    def __str__(self):
        return str(self.id_statistics)


class Developer(models.Model):
    id_developer = models.IntegerField()
    name_developer = models.TextField(max_length=100)

    def __str__(self):
        return str(self.name_developer)


class BugReport(models.Model):
    id_author = models.BigIntegerField()
    nickname_author = models.CharField(max_length=100)
    name_author = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return str(self.date)




