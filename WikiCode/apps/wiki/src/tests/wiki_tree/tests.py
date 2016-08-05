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

from WikiCode.apps.wiki.src.future.wiki_tree import wiki_tree as wt_test

# Version:       0.003
# Total Tests:   0


class WikiTreeTest(object):
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
    # -------------------------------------
    # ТУТ РАСПОЛОГАЕМ ОПИСАНИЕ ТЕСТА
    # def test_1(self):
    #     if 42 == 42:
    #         pass
    #     else:
    #         self.__add_error("1","42 not 42!")
    # test_1(self)
    # -------------------------------------

    # В этой фунции описываем все тесты

    def __tests(self):
        # -------------------------------------
        def test_1(self):
            print("WikiFileTree: " + test_1.__name__)
            wft = wt_test.WikiFileTree()
            if not wft.create_tree(14):
                self.__add_error("1","Arg Error!")
        test_1(self)

        # -------------------------------------
        def test_2(self):
            print("WikiFileTree: " + test_2.__name__)
            wft = wt_test.WikiFileTree()
            if wft.create_tree("asas"):
                self.__add_error("2", "Arg Error!")
        test_2(self)

        # -------------------------------------
        def test_3(self):
            print("WikiFileTree: " + test_3.__name__)
            wft = wt_test.WikiFileTree()
            wft.create_tree(1)
            # wft.print_xml()
        test_3(self)

        # -------------------------------------
        def test_4(self):
            print("WikiFileTree: " + test_4.__name__)
            wft = wt_test.WikiFileTree()
            wft.create_tree(1)
            new_tree = wft.get_xml_str()
            wft.load_tree(new_tree)
            loaded_tree = wft.get_xml_str()
            if new_tree != loaded_tree:
                self.__add_error("4","Not compare for loaded and create trees!")
        test_4(self)

        # -------------------------------------
        def test_5(self):
            print("WikiFileTree: " + test_5.__name__)
            wft = wt_test.WikiFileTree()
            wft.create_tree(3423)
            if wft.get_id() != 3423:
                self.__add_error("5", "get_id is error!")
            wft.create_tree(-212)
            if wft.get_id() != -212:
                self.__add_error("5.1", "get_id is error!")
            wft.create_tree("")
            if wft.get_id() is not None:
                self.__add_error("5.2", "get_id is error!")
            wft.create_tree("asasssa")
            if wft.get_id() is not None:
                self.__add_error("5.3", "get_id is error!")
        test_5(self)

        # -------------------------------------
        def test_6(self):
            print("WikiFileTree: " + test_6.__name__)
            wft = wt_test.WikiFileTree()
            wft.create_tree(1)
            for i in range(0,10):
                k = -1
                if i>3:
                    k = i-1
                status = wft.create_folder(id=i,
                              access="public",
                              type="personal",
                              name="new folder",
                              style="red",
                              view="closed",
                              id_folder=k)
            # wft.print_xml()
        test_6(self)

        # -------------------------------------
        def test_7(self):
            print("WikiFileTree: " + test_7.__name__)
            wft = wt_test.WikiFileTree()
            wft.create_tree(1)
            status = wft.create_folder(id=1,
                                        access="protected",
                                        type="personal",
                                        name="new folder",
                                        style="red",
                                        view="closed",
                                        id_folder=-1)
            if status: self.__add_error("7.1", "create folders error!")

            status = wft.create_folder(id=1,
                                       access="public",
                                       type="personal",
                                       name="new folder",
                                       style="red",
                                       view="open",
                                       id_folder=-1)

            if not status: self.__add_error("7.2", "create folders error!")

            status = wft.create_folder(id=1,
                                       access="private",
                                       type="saved",
                                       name="new folder",
                                       style="green",
                                       view="open",
                                       id_folder=-1)

            if not status: self.__add_error("7.3", "create folders error!")

            status = wft.create_folder(id=1,
                                       access="private",
                                       type="saved",
                                       name="new folder",
                                       style="green",
                                       view="open",
                                       id_folder=2)

            if not status: self.__add_error("7.4", "create folders error!")

            # wft.print_xml()

        test_7(self)






