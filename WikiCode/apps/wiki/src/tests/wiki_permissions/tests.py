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

# ТЕСТИРОВАНИЕ ФУНКЦИОНАЛА WIKIPERMISSIONS

from WikiCode.apps.wiki.src.future.wiki_permissions import wiki_permissions as wp_test

# Version:       0.001
# Total Tests:   0


class WikiPermissionsTest(object):
    # ----- Интерфейс тестов

    def __init__(self):
        self.errors = []

    # Запустить тесты
    def run(self):
        self.__tests()
        return True

    # Вернуть все найденнные ошибки
    def get_errors(self):
        return self.errors

    # ----- Функционал тестов

    # Добавить ошибку
    # Указывается номер теста и сообщение об ошибке
    def __add_error(self, num_test, msg):
        self.errors.append({
            "module": "WikiTree",
            "num_test": num_test,
            "msg": msg
        })

    # Обязательно должен быть порядковый номер теста
    # Тесты не должны принимать никаких аргументов
    # Тесты не могут вызывать другие тесты
    # У всех тестов строго своя область видимости, они не должны обмениваться данными
    # Желательно, чтобы тест вызывал self.__add_error ровно 1 раз
    # Каждый тест должен использовать только тот единственный импорт, что имеется в данном сценарии, а именно wt_test
    # При изменении файла, увеличиваем версию + 1 (В комментарии сверху файла)
    # При добавлении нового теста, увеличиваем количество тестов + 1 (В комментарии сверху файла)
    # В конце теста обязан содержаться его вызов!

    # Пример теста:
    # #-------------------------------------
    # # ТУТ РАСПОЛОГАЕМ ОПИСАНИЕ ТЕСТА
    # def test_1(self):
    #     if 42 == 42:
    #         pass
    #     else:
    #         self.__add_error("1","42 not 42!")
    # test_1(self)
    # #-------------------------------------

    # В этой фунции описываем все тесты

    def __tests(self):
        # -------------------------------------
        # СОЗДАНИЕ СПИСКОВ ДОСТУПА
        def test_1(self):
            print("WikiPermissions: " + test_1.__name__)
            wp = wp_test.WikiPermissions()
            stats = set()
        test_1(self)