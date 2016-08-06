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

# Version:       0.016
# Total Tests:   21


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

        # -------------------------------------
        def test_8(self):
            print("WikiFileTree: " + test_8.__name__)
            wft = wt_test.WikiFileTree()
            stats = set()
            stats.add(wft.create_tree(1))
            stats.add(wft.create_folder(id=1,access="private",type="saved",name="new folder",style="green",view="open",id_folder=-1))
            stats.add(wft.create_folder(id=1.1,access="private",type="saved",name="new folder",style="green",view="open",id_folder=1))
            stats.add(wft.create_folder(id=2,access="private",type="saved",name="new folder",style="green",view="open",id_folder=-1))
            stats.add(wft.create_folder(id=21,access="private",type="saved",name="new folder",style="green",view="open",id_folder=2))
            stats.add(wft.create_folder(id=211,access="private",type="saved",name="new folder",style="green",view="open",id_folder=21))
            stats.add(wft.create_folder(id=2111,access="private",type="saved",name="new folder",style="green",view="open",id_folder=211))
            stats.add(wft.create_folder(id=3,access="private",type="saved",name="new folder",style="green",view="open",id_folder=-1))
            stats.add(wft.delete_folder(1))
            stats.add(wft.delete_folder(3))
            stats.add(wft.delete_folder(2111))
            # wft.print_xml()
            if False in stats:
                self.__add_error("8", "delete tree error!!")

        test_8(self)

        # -------------------------------------
        def test_9(self):
            print("WikiFileTree: " + test_9.__name__)
            wft = wt_test.WikiFileTree()
            stats = set()
            stats.add(wft.delete_folder(4))
            wft.create_tree(1)
            stats.add(wft.delete_folder(1))
            wft.create_folder(id=1, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1)
            wft.create_folder(id=2, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1)
            wft.create_folder(id=3, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1)
            stats.add(wft.delete_folder("asas"))
            stats.add(wft.delete_folder(4))
            stats.add(wft.delete_folder(-3))
            # wft.print_xml()
            if True in stats:
                self.__add_error("9", "delete tree error!!")

        test_9(self)

        # -------------------------------------
        def test_10(self):
            print("WikiFileTree: " + test_10.__name__)
            wft = wt_test.WikiFileTree()
            # wft.print_config()

        test_10(self)

        # -------------------------------------
        def test_11(self):
            print("WikiFileTree: " + test_11.__name__)
            wft = wt_test.WikiFileTree()
            stats = set()
            stats.add(wft.create_tree(1))
            stats.add(wft.create_folder(id=1, access="private", type="saved", name="new folder", style="green", view="open", id_folder=-1))
            stats.add(wft.create_folder(id=2, access="private", type="saved", name="new folder", style="green", view="open", id_folder=-1))
            stats.add(wft.create_folder(id=3, access="private", type="saved", name="new folder", style="green", view="open", id_folder=1))
            stats.add(wft.rename_folder(1, "cool folder!"))
            stats.add(wft.rename_folder(2, "bad folder!"))
            stats.add(not wft.rename_folder(7, "bad folder!"))
            stats.add(not wft.rename_folder(1, 1))
            stats.add(not wft.rename_folder(4, 1))
            stats.add(not wft.rename_folder(1, "Hi 'planet'!"))
            stats.add(wft.rename_folder(3, "simple text"))
            # wft.print_xml()
            if False in stats:
                self.__add_error("11", "rename_folder error!")

        test_11(self)

        # -------------------------------------
        def test_12(self):
            print("WikiFileTree: " + test_12.__name__)
            wft = wt_test.WikiFileTree()
            stats = set()
            stats.add(wft.create_tree(1))
            stats.add(wft.create_folder(id=1, access="private", type="saved", name="new folder", style="green", view="open", id_folder=-1))
            stats.add(wft.create_folder(id=2, access="private", type="saved", name="new folder", style="green", view="open", id_folder=-1))
            stats.add(wft.create_folder(id=3, access="private", type="saved", name="new folder", style="green", view="open", id_folder=1))
            stats.add(wft.create_folder(id=4, access="private", type="saved", name="new folder", style="green", view="open", id_folder=3))
            stats.add(wft.reaccess_folder(1, "public"))
            stats.add(wft.reaccess_folder(2, "public"))
            stats.add(not wft.reaccess_folder(8, "public"))
            stats.add(not wft.reaccess_folder(1, 1))
            stats.add(not wft.reaccess_folder(4, 1))
            stats.add(wft.reaccess_folder(4, "public"))
            stats.add(not wft.reaccess_folder(1, "strange"))
            stats.add(wft.reaccess_folder(3, "public"))
            # wft.print_xml()
            if False in stats:
                self.__add_error("12", "reaccess_folder error!")

        test_12(self)

        # -------------------------------------
        def test_13(self):
            print("WikiFileTree: " + test_13.__name__)
            wft = wt_test.WikiFileTree()
            stats = set()
            stats.add(wft.create_tree(1))
            stats.add(wft.create_folder(id=1, access="private", type="saved", name="new folder", style="green", view="open", id_folder=-1))
            stats.add(wft.create_folder(id=2, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=3, access="private", type="saved", name="new folder", style="green", view="open",id_folder=1))
            stats.add(wft.create_folder(id=4, access="private", type="saved", name="new folder", style="green", view="open",id_folder=3))
            stats.add(wft.retype_folder(1, "saved"))
            stats.add(wft.retype_folder(2, "saved"))
            stats.add(not wft.retype_folder(8, "saved"))
            stats.add(not wft.retype_folder(1, 1))
            stats.add(not wft.retype_folder(4, 1))
            stats.add(wft.retype_folder(4, "saved"))
            stats.add(not wft.retype_folder(1, "strange"))
            stats.add(wft.retype_folder(3, "saved"))
            # wft.print_xml()
            if False in stats:
                self.__add_error("13", "retype_folder error!")

        test_13(self)

        # -------------------------------------
        def test_14(self):
            print("WikiFileTree: " + test_14.__name__)
            wft = wt_test.WikiFileTree()
            stats = set()
            stats.add(wft.create_tree(1))
            stats.add(wft.create_folder(id=1, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=2, access="private", type="saved", name="  new folder  ", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=3, access="private", type="saved", name="new folder", style="green", view="open",id_folder=1))
            stats.add(wft.create_folder(id=4, access="private", type="saved", name="new folder", style="green", view="open",id_folder=3))
            stats.add(wft.restyle_folder(1, "red"))
            stats.add(wft.restyle_folder(2, "blue"))
            stats.add(not wft.restyle_folder(8, "red"))
            stats.add(not wft.restyle_folder(1, 1))
            stats.add(not wft.restyle_folder(4, 1))
            stats.add(wft.restyle_folder(4, "default"))
            stats.add(not wft.restyle_folder(1, "strange"))
            stats.add(wft.restyle_folder(3, "red"))
            # wft.print_xml()
            if False in stats:
                self.__add_error("14", "restyle_folder error!")

        test_14(self)

        # -------------------------------------
        def test_15(self):
            print("WikiFileTree: " + test_15.__name__)
            wft = wt_test.WikiFileTree()
            stats = set()
            stats.add(wft.create_tree(1))
            stats.add(wft.create_folder(id=2, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=1, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=3, access="private", type="saved", name="new folder", style="green", view="open",id_folder=1))
            stats.add(wft.create_folder(id=4, access="private", type="saved", name="new folder", style="green", view="open",id_folder=3))
            stats.add(wft.review_folder(1, "closed"))
            stats.add(wft.review_folder(2, "closed"))
            stats.add(not wft.review_folder(8, "closed"))
            stats.add(not wft.review_folder(1, 1))
            stats.add(not wft.review_folder(4, 1))
            stats.add(wft.review_folder(4, "closed"))
            stats.add(not wft.review_folder(1, "strange"))
            stats.add(wft.review_folder(3, "closed"))
            # wft.print_xml()
            if False in stats:
                self.__add_error("15", "review_folder error!")

        test_15(self)

        # -------------------------------------
        def test_16(self):
            print("WikiFileTree: " + test_16.__name__)
            wft = wt_test.WikiFileTree()
            stats = set()
            stats.add(wft.create_tree(1))
            stats.add(wft.create_folder(id=2, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=1, access="private", type="saved", name="  new folder  ", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=3, access="private", type="saved", name="new folder", style="green", view="open",id_folder=1))
            stats.add(wft.create_folder(id=4, access="private", type="saved", name="new folder", style="green", view="open",id_folder=3))
            stats.add(wft.create_publication(id=17, id_folder=2, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=18, id_folder=2, access="public", type="personal", name="Уроки по С++ "))
            stats.add(wft.create_publication(id=19, id_folder=5, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=42, id_folder=-1, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=42, id_folder=-1, access="private", type="personal", name=" Уроки по С++"))
            stats.add(not wft.create_publication(id=42, id_folder=-1, access="private", type="saved", name=" "))
            stats.add(not wft.create_publication(id=42, id_folder=-1, access="private", type="saved", name="'"))
            stats.add(wft.create_publication(id=42, id_folder=-1, access="private", type="saved", name="   new lesson!"))

            # wft.print_xml()
            if False in stats:
                self.__add_error("16", "review_folder error!")

        test_16(self)

        # -------------------------------------
        def test_17(self):
            print("WikiFileTree: " + test_17.__name__)
            wft = wt_test.WikiFileTree()
            stats = set()
            wft.create_tree(1)
            stats.add(wft.create_folder(id=1, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=2, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=3, access="private", type="saved", name="new folder", style="green", view="open",id_folder=1))
            stats.add(wft.create_publication(id=17, id_folder=1, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=18, id_folder=2, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=19, id_folder=3, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=42, id_folder=-1, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=43, id_folder=-1, access="public", type="personal", name="Уроки по С++"))
            stats.add(not wft.delete_folder(4))
            stats.add(wft.delete_publication(43))
            stats.add(wft.delete_publication(42))
            stats.add(wft.delete_publication(18))
            stats.add(wft.delete_publication(17))
            stats.add(wft.delete_publication(19))
            stats.add(not wft.delete_publication(20))
            stats.add(wft.delete_folder(1))
            stats.add(wft.delete_folder(2))
            stats.add(not wft.delete_folder(3))
            # wft.print_xml()
            if False in stats:
                self.__add_error("17", "delete tree error!!")

        test_17(self)

        def test_18(self):
            print("WikiFileTree: " + test_18.__name__)
            wft = wt_test.WikiFileTree()
            stats = set()
            wft.create_tree(1)
            stats.add(not wft.create_folder(id=2, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(not wft.create_folder(id=3, access="private", type="saved", name="new folder", style="green", view="open",id_folder=1))
            stats.add(not wft.create_folder(id=1, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(not wft.create_publication(id=17, id_folder=1, access="public", type="personal", name="Уроки по С++"))
            stats.add(not wft.create_publication(id=18, id_folder=2, access="public", type="personal", name="Уроки по С++"))
            stats.add(not wft.create_publication(id=19, id_folder=3, access="public", type="personal", name="Уроки по С++"))
            stats.add(not wft.create_publication(id=42, id_folder=-1, access="public", type="personal", name="Уроки по С++"))
            stats.add(not wft.create_publication(id=43, id_folder=-1, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.delete_publication("sadsa"))
            stats.add(wft.delete_publication(46))
            stats.add(not wft.delete_publication(42))
            stats.add(wft.delete_publication(42))
            stats.add(not wft.create_publication(id=42, id_folder=-1, access="public", type="personal", name="Уроки по С++"))
            stats.add(not wft.delete_publication(42))
            # wft.print_xml()
            if True in stats:
                self.__add_error("18", "delete tree error!!")

        test_18(self)

        # -------------------------------------
        def test_19(self):
            print("WikiFileTree: " + test_19.__name__)
            wft = wt_test.WikiFileTree()
            stats = set()
            stats.add(wft.create_tree(1))
            stats.add(wft.create_folder(id=1, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=2, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=3, access="private", type="saved", name="new folder", style="green", view="open",id_folder=1))
            stats.add(wft.create_publication(id=17, id_folder=1, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=18, id_folder=2, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=19, id_folder=3, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=42, id_folder=-1, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=43, id_folder=-1, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.rename_folder(1, "cool folder!"))
            stats.add(not wft.rename_publication(1, "cool folder!"))
            stats.add(wft.rename_publication(17, "Уроки по Java"))
            stats.add(wft.rename_publication(18, "Уроки по Scala"))
            stats.add(wft.rename_publication(18, "Уроки по Clojure"))
            stats.add(wft.rename_publication(18, " Уроки по Clojure  "))
            stats.add(wft.rename_publication(43, "Уроки по Python"))
            stats.add(not wft.rename_publication(43, "Уроки по 'Python'"))
            stats.add(not wft.rename_publication(43, ""))
            stats.add(not wft.rename_publication(43, 111))
            stats.add(not wft.rename_publication(43, "   "))
            stats.add(not wft.rename_publication(43, "  ' "))
            # wft.print_xml()
            if False in stats:
                self.__add_error("19", "rename_publication error!")

        test_19(self)

        # -------------------------------------
        def test_20(self):
            print("WikiFileTree: " + test_20.__name__)
            wft = wt_test.WikiFileTree()
            stats = set()
            stats.add(wft.create_tree(1))
            stats.add(wft.create_folder(id=1, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=2, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=3, access="private", type="saved", name="new folder", style="green", view="open",id_folder=1))
            stats.add(wft.create_publication(id=17, id_folder=1, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=18, id_folder=2, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=19, id_folder=3, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=43, id_folder=-1, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=42, id_folder=-1, access="public", type="personal", name="Уроки по С++"))
            stats.add(not wft.reaccess_publication(1, "public"))
            stats.add(wft.reaccess_publication(17, "private"))
            stats.add(not wft.reaccess_publication(18, "privatebl"))
            stats.add(wft.reaccess_publication(18, "private"))
            stats.add(not wft.reaccess_publication(18, "private'"))
            stats.add(not wft.reaccess_publication(18, ""))
            stats.add(not wft.reaccess_publication(18, 1))
            stats.add(not wft.reaccess_publication("private", "private"))
            stats.add(not wft.reaccess_publication("", "private"))
            stats.add(wft.reaccess_publication(42, "public"))
            stats.add(wft.reaccess_publication(42, "private"))
            # wft.print_xml()
            if False in stats:
                self.__add_error("20", "reaccess_publication error!")

        test_20(self)

        # -------------------------------------
        def test_21(self):
            print("WikiFileTree: " + test_21.__name__)
            wft = wt_test.WikiFileTree()
            stats = set()
            stats.add(wft.create_tree(1))
            stats.add(wft.create_folder(id=2, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=1, access="private", type="saved", name="new folder", style="green", view="open",id_folder=-1))
            stats.add(wft.create_folder(id=3, access="private", type="saved", name="new folder", style="green", view="open",id_folder=1))
            stats.add(wft.create_publication(id=17, id_folder=1, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=18, id_folder=2, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=19, id_folder=3, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=43, id_folder=-1, access="public", type="personal", name="Уроки по С++"))
            stats.add(wft.create_publication(id=42, id_folder=-1, access="public", type="personal", name="Уроки по С++"))
            stats.add(not wft.retype_publication(1, "personal"))
            stats.add(wft.retype_publication(17, "saved"))
            stats.add(not wft.retype_publication(18, "savedbl"))
            stats.add(wft.retype_publication(18, "saved"))
            stats.add(not wft.retype_publication(18, "saved'"))
            stats.add(not wft.retype_publication(18, ""))
            stats.add(not wft.retype_publication(18, 1))
            stats.add(not wft.retype_publication("saved", "saved"))
            stats.add(not wft.retype_publication("", "saved"))
            stats.add(wft.retype_publication(42, "personal"))
            stats.add(wft.retype_publication(42, "saved"))
            # wft.print_xml()
            if False in stats:
                self.__add_error("21", "retype_publication error!")

        test_21(self)





