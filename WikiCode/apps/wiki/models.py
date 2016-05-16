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
    saved_publ = models.TextField()
    likes = models.BigIntegerField()
    publications = models.BigIntegerField()
    imports = models.BigIntegerField()
    comments = models.BigIntegerField()
    imports_it = models.BigIntegerField()
    commented_it = models.BigIntegerField()
    avatar = models.ImageField(upload_to='avatars')
    preview_publ_id = models.BigIntegerField()
    def __str__(self):
        return str(self.id_user)


# Коллега
class Colleague(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_colleague = models.BigIntegerField()
    is_favorit = models.BooleanField()
    def __str__(self):
        return str("user:" + str(self.id_user) +
               " colleague:" + str(self.id_colleague))


class Like(models.Model):
    id_user = models.BigIntegerField()
    nickname = models.CharField(max_length=100)
    type = models.CharField(max_length=100) # Тип либо publ, либо user
    id_publ_like = models.BigIntegerField(blank=True)
    id_user_like = models.BigIntegerField(blank=True)
    date = models.CharField(max_length=100)
    def __str__(self):
        return str("user:"+str(self.id_user)+
                   " type:"+str(self.type)+
                   " publ-like:"+str(self.id_publ_like)+
                   " user-like:"+str(self.id_user_like))


class Publication(models.Model):
    id_publication = models.BigIntegerField()
    id_author = models.BigIntegerField()
    nickname_author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    text = models.TextField()
    theme = models.CharField(max_length=50)
    html_page = models.TextField()
    is_private = models.BooleanField()
    is_public = models.BooleanField()
    is_private_edit = models.BooleanField()
    is_public_edit = models.BooleanField()
    is_marks = models.BooleanField()
    is_comments = models.BooleanField()
    tags = models.TextField()
    tree_path = models.TextField()
    comments = models.BigIntegerField()
    imports = models.BigIntegerField()
    marks = models.BigIntegerField()
    likes = models.BigIntegerField()
    read = models.BigIntegerField()
    edits = models.BigIntegerField()
    downloads = models.BigIntegerField()
    def __str__(self):
        return str(self.id_publication)

# Модель редактора публикации
class Editor(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    id_user = models.BigIntegerField()
    nickname_user = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    def __str__(self):
        return str("user:" + str(self.id_user) +
                   " publ:" + str(self.publication))


# Модель просмотра страницы. Указывает кто просмотрел и когда
class Viewing(models.Model):
    id_user = models.BigIntegerField()
    nickname = models.CharField(max_length=100)
    id_publ = models.BigIntegerField()
    date = models.CharField(max_length=100)
    def __str__(self):
        return str("user:" + str(self.id_user) +
                   " publ:" + str(self.id_publ))

class CommentBlock(models.Model):
    id_publication = models.BigIntegerField()
    last_id = models.BigIntegerField()
    def __str__(self):
        return str(self.id_publication)


class Comment(models.Model):
    comment_block = models.ForeignKey(CommentBlock, on_delete=models.CASCADE)
    num_position = models.BigIntegerField()
    id_author = models.BigIntegerField()
    nickname_author = models.CharField(max_length=100)
    rating = models.BigIntegerField()
    text = models.TextField()
    data = models.CharField(max_length=100)
    id_author_answer = models.BigIntegerField()
    nickname_author_answer = models.CharField(max_length=100)
    def __str__(self):
        return str(self.comment_block)

# Единый набор всех динамичных параграфов для одного конспекта
class Paragraphs(models.Model):
    id_publication = models.BigIntegerField()
    last_id = models.BigIntegerField()
    def __str__(self):
        return str(self.id_publication)


# Отдельный динамический параграф в конспекте
class DynamicCommentParagraph(models.Model):
    paragraphs = models.ForeignKey(Paragraphs, on_delete=models.CASCADE)
    num_position = models.BigIntegerField()
    is_comment = models.BooleanField(default=False)
    last_id = models.BigIntegerField()
    def __str__(self):
        return str(str(self.paragraphs)+"_"+str(self.num_position))


# Отдельный динамичный комментарий
class DynamicComment(models.Model):
    dynamic_comment_paragraph = models.ForeignKey(DynamicCommentParagraph, on_delete=models.CASCADE)
    num_position = models.BigIntegerField()
    id_author = models.BigIntegerField()
    nickname_author = models.CharField(max_length=100)
    text = models.TextField()
    data = models.CharField(max_length=100)
    def __str__(self):
        return str(str(self.dynamic_comment_paragraph)+"_"+str(self.num_position))


class Statistics(models.Model):
    id_statistics = models.IntegerField()
    # Зарегестрировано юзеров
    users_reg = models.BigIntegerField()
    # Зарегестрировано юзеров за всю историю
    users_total_reg = models.BigIntegerField(default=0)
    user_online = models.BigIntegerField()
    publications_create = models.BigIntegerField()
    publications_delete = models.BigIntegerField()
    publications_active = models.BigIntegerField()
    publications_private = models.BigIntegerField()
    publications_public = models.BigIntegerField()
    comments = models.BigIntegerField()
    notifications = models.BigIntegerField()
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




