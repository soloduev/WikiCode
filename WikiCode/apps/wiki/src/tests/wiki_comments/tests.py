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

from WikiCode.apps.wiki.src.modules.wiki_comments import wiki_comments as wc_test

# Version:       0.011
# Total Tests:   11


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

        # -------------------------------------
        # Проверка на создание нового комментария
        def test_5(self):
            print("WikiComments: " + test_5.__name__)
            wc = wc_test.WikiComments()
            wc.create_comments(1)
            wc.create_comment(1,2,"Hello!","Boris","17.08.2017",False)
            wc.create_comment(16,4,"Hi!","Katya","20.08.2017",False)
            wc.create_comment(26,8,"How are you?","Petya","21.08.2017",False)
            # wc.print_xml()

        test_5(self)

        # -------------------------------------
        # Проверка на редакатирование комментария
        def test_6(self):
            print("WikiComments: " + test_6.__name__)
            wc = wc_test.WikiComments()
            wc.create_comments(1)
            states = set()
            states.add(wc.create_comment(1, 2, "Hello!", "Boris", "17.08.2017", False))
            states.add(wc.create_comment(16, 4, "Hi!", "Katya", "20.08.2017", False))
            states.add(wc.create_comment(26, 8, "How are you?", "Petya", "21.08.2017", False))
            states.add(wc.edit_comment(16, "Bye!", "20.08.2017"))
            states.add(not wc.edit_comment(15, "Bye!", "20.08.2017"))

            if False in states:
                self.__add_error("6", "Edit comments")

            # wc.print_xml()

        test_6(self)

        # -------------------------------------
        # Проверка на удаление комментария
        def test_7(self):
            print("WikiComments: " + test_7.__name__)
            wc = wc_test.WikiComments()
            wc.create_comments(1)
            states = set()
            states.add(wc.create_comment(1, 2, "Hello!", "Boris", "17.08.2017", False))
            states.add(wc.create_comment(16, 4, "Hi!", "Katya", "20.08.2017", False))
            states.add(wc.create_comment(26, 8, "How are you?", "Petya", "21.08.2017", False))
            states.add(wc.delete_comment(26))
            states.add(wc.delete_comment(16))
            states.add(not wc.delete_comment(2))

            if False in states:
                self.__add_error("7", "Delete comments")

            # wc.print_xml()

        test_7(self)

        # -------------------------------------
        # Проверка ответа на комментарий
        def test_8(self):
            print("WikiComments: " + test_8.__name__)
            wc = wc_test.WikiComments()
            wc.create_comments(1)
            states = set()
            states.add(wc.create_comment(1, 2, "Hello!", "Boris", "17.08.2017", False))
            states.add(wc.create_comment(16, 4, "Hi!", "Katya", "20.08.2017", False))
            states.add(wc.create_comment(26, 8, "How are you?", "Petya", "21.08.2017", False))
            states.add(wc.reply(70,4,"Vasya","Good",26,"14.09.2017",False))
            states.add(wc.reply(74,4,"Vasya","Perfect!",26,"14.09.2017",False))
            states.add(wc.reply(77,5,"Nastya","And you?",74,"14.09.2017",False))
            states.add(wc.reply(78,4,"Vasya","Very good",77,"14.09.2017",False))
            states.add(not wc.reply(80,4,"Borya","Bad",25,"14.09.2017",False))

            if False in states:
                self.__add_error("8", "Reply comments")

            # wc.print_xml()

        test_8(self)

        # -------------------------------------
        # Проверка функция complain, up_rating, down_rating
        def test_9(self):
            print("WikiComments: " + test_9.__name__)
            wc = wc_test.WikiComments()
            wc.create_comments(1)
            states = set()
            states.add(wc.create_comment(1, 2, "Hello!", "Boris", "17.08.2017", False))
            states.add(wc.create_comment(16, 4, "Hi!", "Katya", "20.08.2017", False))
            states.add(wc.create_comment(26, 8, "How are you?", "Petya", "21.08.2017", False))
            states.add(wc.complain(16))
            states.add(not wc.complain(25))
            states.add(wc.up_rating(1))
            states.add(wc.up_rating(1))
            states.add(wc.up_rating(1))
            states.add(wc.down_rating(1))
            states.add(wc.down_rating(16))
            states.add(not wc.down_rating(17))

            if False in states:
                self.__add_error("9", "Claim/rating comments")

            # wc.print_xml()

        test_9(self)

        # -------------------------------------
        # Проверка отладочных функций
        def test_10(self):
            print("WikiComments: " + test_10.__name__)
            wc = wc_test.WikiComments()
            wc.create_comments(1)
            states = set()
            states.add(wc.create_comment(1, 2, "Hello!", "Boris", "17.08.2017", False))
            states.add(wc.create_comment(16, 4, "Hi!", "Katya", "20.08.2017", False))
            states.add(wc.create_comment(26, 8, "How are you?", "Petya", "21.08.2017", False))
            # states.add(wc.print_comment(16))
            states.add(not wc.print_comment(2))
            # print(wc.debug_comment(16))
            # print(wc.debug_comment(2))

            if False in states:
                self.__add_error("10", "Claim/rating comments")

        test_10(self)

        # -------------------------------------
        # Проверка генерации html
        def test_11(self):
            print("WikiComments: " + test_11.__name__)
            wc = wc_test.WikiComments()
            wc.create_comments(1)

            wc.create_comment(1, 2, "Hello!", "Boris", "17.08.2017", False)
            wc.create_comment(16, 4, "Hi!", "Katya", "20.08.2017", False)
            wc.create_comment(26, 8, "How are you?", "Petya", "21.08.2017", False)
            wc.reply(30,30,"Borya","hff",1,"23.02.2010",False)
            wc.reply(33,30,"Borya","hff2",1,"23.02.2010",False)
            wc.reply(35,33,"Borya","333",33,"23.02.2010",False)
            # wc.print_xml()
            # print(wc.to_html())


        test_11(self)






