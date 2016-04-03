from django.contrib import admin
from .models import User
from .models import Publication, Statistics
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
