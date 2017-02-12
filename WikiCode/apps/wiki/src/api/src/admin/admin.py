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


# Администрирование платформы

from WikiCode.apps.wiki.src.api.src import djangoapi as __djangoapi


# Данный метод генерирует необходимое количество invite ключей, а также модели к ним.
# На вход передается один обязательный параметр - необходимое количество сгенерированных invite ключей
# По соображениям безопасности, сгенерировать за 1 раз больше 10 ключей нельзя.
def generate_invite_keys(count):
    try:
        num = int(count)
        if num < 1 or num > 10:
            print("Тип передаваемого параметра должен быть положительным целым числом в диапазоне от 1 до 10")
        else:
            print("Список сгенерированных ключей:")
            gen_chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789"
            for n in range(0, num):
                result_key = ""
                for i in range(0, 16):
                    index_char = __djangoapi.random.randrange(0, len(gen_chars))
                    result_key += gen_chars[index_char]
                print(result_key)
                new_key = __djangoapi.InviteKeys(key=result_key)
                new_key.save()
    except ValueError:
        print("Тип передаваемого параметра должен быть числом")