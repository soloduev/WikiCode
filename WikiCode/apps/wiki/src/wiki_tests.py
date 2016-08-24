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


# МОДУЛЬ ТЕСТИРОВАНИЯ ПЛАТФОРМЫ

# Запускает все тесты по очереди
# Если какой то из них не успешен, платформа не запускается

# Запускается этот модуль из файла manage.py
# Для работы с этим модулем, необходимо в настройках платформы(settings/wiki_setting.py) прописать RUN_TESTS = True
# И затем, если этот модуль запущен, просто стандартно запускать manage.py.

# Подклучаем все тестирующие программы сюда

from WikiCode.apps.wiki.src.tests.wiki_markdown.tests import WikiMarkdownTest
from WikiCode.apps.wiki.src.tests.wiki_tree.tests import WikiTreeTest
from WikiCode.apps.wiki.src.tests.wiki_comments.tests import WikiCommentsTest
from WikiCode.apps.wiki.src.tests.wiki_permissions.tests import WikiPermissionsTest


# WIKI_TEST.    Version 0.3


class WikiTests(object):
    def run(self):

        print()
        print("-------------------------------------------")
        print("----- Wiki test started. Please wait. -----")
        print("-------------------------------------------")
        print()

        # Все ошибки которые получим
        errors = []

        # Создаем экземпляры тестирующих модулей
        # Необходимо добавить переменную теста, для тестирования нового модуля
        wmt = WikiMarkdownTest()
        wtt = WikiTreeTest()
        wct = WikiCommentsTest()
        wpt = WikiPermissionsTest()

        # Запускаем тесты
        # При добавлении нового теста, необходимо его запустить
        wmt.run()
        wtt.run()
        wct.run()
        wpt.run()

        # Получаем ошибки с этих тестов
        # Также, при добавлении нового теста, необходимо считать с него ошибки
        for err in wmt.get_errors(): errors.append(err)
        for err in wtt.get_errors(): errors.append(err)
        for err in wct.get_errors(): errors.append(err)
        for err in wpt.get_errors(): errors.append(err)

        # Проверяем на наличие ошибок
        # Если ошибок нет
        if len(errors) == 0:

            print()
            print("-------------------------------------------")
            print("Wiki test completed! Errors does not exist!")
            print("-------------------------------------------")
            print()

            return True

        # Если они есть, печатаем логи
        else:

            print()
            print("LIST ERRORS:")
            print()

            for error in errors:
                print(str(error["module"]) + " |", str(error["num_test"]) + " | ", str(error["msg"]))

            print()
            print("FOUND " + str(len(errors)) + " ERRORS")
            print()

            return False
