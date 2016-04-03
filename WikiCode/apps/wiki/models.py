from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    user = models.OneToOneField(DjangoUser)
    id_user = models.BigIntegerField()
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    likes = models.BigIntegerField()
    publications = models.BigIntegerField()
    imports = models.BigIntegerField()
    comments = models.BigIntegerField()
    imports_it = models.BigIntegerField()
    commented_it = models.BigIntegerField()
    avatar = models.ImageField(upload_to='avatars')
    def __str__(self):
        return str(self.id_user)


class Publication(models.Model):
    id_publication = models.BigIntegerField()
    id_author = models.BigIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    text = models.TextField()
    theme = models.CharField(max_length=50)
    html_page = models.FileField(upload_to='publications')
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
    def __str__(self):
        return str(self.id_publication)


class Comment(models.Model):
    id_comment = models.BigIntegerField()
    id_author = models.BigIntegerField()
    id_publication = models.BigIntegerField()
    date = models.DateTimeField()
    text = models.TextField()
    addressee = models.CharField(max_length=100,blank=True)
    position = models.CharField(max_length=100) # right, left, down
    height = models.IntegerField(blank=True)
    def __str__(self):
        return str(self.id_comment)


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


class Notification(models.Model):
    id_notification = models.BigIntegerField()
    id_author = models.BigIntegerField()
    id_publication = models.BigIntegerField()
    author_to = models.BigIntegerField()
    type = models.CharField(max_length=100)
    text = models.TextField()
    def __str__(self):
        return str(self.id_notification)






