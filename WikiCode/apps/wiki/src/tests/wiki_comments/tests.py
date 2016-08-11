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

# ТЕСТИРОВАНИЕ ФУНКЦИОНАЛА WIKICOMMENTS

from WikiCode.apps.wiki.src.future.wiki_comments import wiki_comments as wc_test

# Version:       0.004
# Total Tests:   3


class WikiCommentsTest(object):
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
        # СОЗДАНИЕ КОММЕНТАРИЕВ
        def test_1(self):
            print("WikiComments: " + test_1.__name__)
            wc = wc_test.WikiComments()
            stats = set()
            stats.add(wc.create_comments(1))
            stats.add(wc.create_comments(-1))
            stats.add(wc.create_comments(0))
            stats.add(wc.create_comments(324324))
            stats.add(not wc.create_comments("asas"))
            if False in stats:
                self.__add_error("1", "Create comments error")
        test_1(self)

        # -------------------------------------
        # ЗАГРУЗКА КОММЕНТАРИЕВ
        def test_2(self):
            print("WikiComments: " + test_2.__name__)
            wc = wc_test.WikiComments()
            wc.create_comments(1)
            xml_str_1 = wc.get_xml_str()
            wc.load_comments(xml_str_1)
            xml_str_2 = wc.get_xml_str()
            # print(xml_str_1)
            # print()
            # print(xml_str_2)

        test_2(self)

        # -------------------------------------
        # Проверка id
        def test_3(self):
            print("WikiComments: " + test_3.__name__)
            wc = wc_test.WikiComments()
            wc.create_comments(1)
            if wc.get_id() != 1: self.__add_error("3", "id error!")
            wc.create_comments("sadfsad")
            if wc.get_id() != None: self.__add_error("3", "id error!")
        test_3(self)

        # -------------------------------------
        # Проверка на использование функции создания комментариев
        def test_4(self):
            print("WikiComments: " + test_4.__name__)
            wc = wc_test.WikiComments()
            if wc.create_comment(1,3,"dsgfhdsfdsf","Hellen","332432",False):
                self.__add_error("4", "Error create comments!")

        test_4(self)







