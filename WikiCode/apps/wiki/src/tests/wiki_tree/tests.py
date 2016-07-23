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

# ТЕСТИРОВАНИЕ ФУНКЦИОНАЛА WIKITREE

from WikiCode.apps.wiki.src.wiki_tree import WikiTree as wt_test

# Version:       0.002
# Total Tests:   0


class WikiTreeTest(object):
    # ----- Интерфейс тестов

    def __init__(self):
        self.errors = []

    # Запустить тесты
    def run(self):
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

        # ----- Сами тесты. Номера идут по порядку
        # ----- Добавляя тест, его нужно прописать в run
        # ----- Каждый тест не должен ничего возвращать
        # ----- Если в нем ошибка, то добавляем ее с помощью self.__add_error

        # Обязательно должен быть порядковый номер теста
        # Обязательно должен быть комментарий к тесту
        # Все тесты должны быть упакованы строго по порядку в функцию run() и названия всех тестов должны отличаться
        # Использовать один и тот же тест строго запрещено
        # Тесты не должны принимать никаких аргументов
        # Тесты не могут вызывать другие тесты
        # У всех тестов строго своя область видимости, они не должны обмениваться данными
        # Желательно, чтобы тест вызывал self.__add_error ровно 1 раз
        # Каждый тест должен использовать только тот единственный импорт, что имеется в данном сценарии, а именно wt_test
        # При изменении файля, увеличиваем версию + 1 (В комментарии сверху файла)
        # При добавлении нового теста, увеличиваем количество тестов + 1 (В комментарии сверху файла)
        # Тест обязан быть приватным

        # Пример теста:

        # def __test_1(self):
        #     """Проверяем, равно ли сорок два, сорока двум""
        #     if 42 == 42:
        #         pass
        #     else:
        #         self.__add_error("1","42 not 42!")