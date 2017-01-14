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

from django.contrib import admin
from .models import User
from .models import Publication
from .models import Statistics
from .models import Viewing
from .models import Developer
from .models import BugReport
from .models import DynamicParagraph
from .models import Comment
from .models import Folder
from .models import Colleague
from .models import Notification
from .models import Starring
from .models import CommentRating
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as DjangoUser

# Register your models here.


class UserInline(admin.StackedInline):
    model = User
    can_delete = False


# Определяем новый класс настроек для модели User
class UserAdmin(UserAdmin):
    inlines = (UserInline, )

# Перерегистрируем модель User
admin.site.unregister(DjangoUser)
admin.site.register(DjangoUser, UserAdmin)

admin.site.register(Publication)
admin.site.register(Statistics)
admin.site.register(Viewing)
admin.site.register(Starring)
admin.site.register(Developer)
admin.site.register(BugReport)
admin.site.register(DynamicParagraph)
admin.site.register(Comment)
admin.site.register(Folder)
admin.site.register(Colleague)
admin.site.register(Notification)
admin.site.register(CommentRating)
