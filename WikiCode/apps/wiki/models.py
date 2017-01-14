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
    file_tree = models.TextField()
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
    description = models.TextField(max_length=500, blank=True)
    text = models.TextField()
    theme = models.CharField(max_length=50)
    html_page = models.TextField()
    tree_path = models.TextField()
    read = models.BigIntegerField()
    stars = models.BigIntegerField()
    saves = models.BigIntegerField()
    main_comments = models.TextField()
    versions = models.BinaryField(blank=True)
    permissions = models.TextField()
    # Все настройки конспекта
    is_public = models.BooleanField()
    is_dynamic_paragraphs = models.BooleanField()
    is_general_comments = models.BooleanField()
    is_contents = models.BooleanField()
    is_protected_edit = models.BooleanField()
    is_files = models.BooleanField()
    is_links = models.BooleanField()
    is_versions = models.BooleanField()
    is_show_author = models.BooleanField()
    is_loading = models.BooleanField()
    is_saving = models.BooleanField()
    is_starring = models.BooleanField()
    is_file_tree = models.BooleanField()

    def __str__(self):
        return str(self.id_publication)


# Модель отдельного динамического параграфа.
# Пока он используется только для оставления комментариев
class DynamicParagraph(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    paragraph = models.BigIntegerField()
    comments = models.TextField()

    def __str__(self):
            return str(self.publication) + "_" + str(self.paragraph)


# Модель просмотра страницы. Указывает кто просмотрел и когда
class Viewing(models.Model):
    id_user = models.BigIntegerField()
    nickname = models.CharField(max_length=100)
    id_publ = models.BigIntegerField()
    date = models.CharField(max_length=100)

    def __str__(self):
        return str("user:" + str(self.id_user) +
                   " publ:" + str(self.id_publ))


# Указывает кто поставил звезду и когда
class Starring(models.Model):
    id_user = models.BigIntegerField()
    id_publ = models.BigIntegerField()
    date = models.CharField(max_length=100)

    def __str__(self):
        return str("user:" + str(self.id_user) +
                   " publ:" + str(self.id_publ))


class CommentRating(models.Model):
    id_user = models.BigIntegerField()
    id_comment = models.BigIntegerField()
    id_user_to = models.BigIntegerField()  # id пользователя, которому поставили лайк
    type = models.CharField(max_length=4)  # up, down, none

    def __str__(self):
        return str("user:" + str(self.id_user) +
                   " comment:" + str(self.id_comment))


# Модель любого комментария
class Comment(models.Model):
    id_comment = models.BigIntegerField()
    id_author = models.BigIntegerField()
    id_publication = models.BigIntegerField()
    date = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return str("id:" + str(self.id_comment))


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
    user_online = models.BigIntegerField()
    publications_create = models.BigIntegerField()
    total_comments = models.BigIntegerField()   # Всего создано комментариев
    total_folders = models.BigIntegerField()    # Всего создано папок
    total_notification = models.BigIntegerField()  # Всего создано уведомлений
    total_dynamic_comments = models.BigIntegerField()  # Всего инстанциировано блоков динамических комментариев

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


class Colleague(models.Model):
    id_user = models.BigIntegerField()
    id_colleague = models.BigIntegerField()

    def __str__(self):
        return str(self.id_user) + "_" + str(self.id_colleague)


class Notification(models.Model):
    id_notification = models.BigIntegerField()
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    id_sender = models.BigIntegerField()
    id_addressee = models.BigIntegerField()
    is_read = models.BooleanField()
    date = models.CharField(max_length=50)
    html_text = models.TextField()

    def __str__(self):
        return str(self.title) + "; " + str(self.id_sender) + "; " + str(self.id_addressee) + "; " + str(self.date)