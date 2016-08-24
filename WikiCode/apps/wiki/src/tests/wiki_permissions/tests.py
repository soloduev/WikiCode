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

# Version:       0.006
# Total Tests:   9


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
            stats.add(wp.create_permissions(1, 42))
            # wp.print_xml()

            if False in stats:
                self.__add_error("1", "Create permissions error")

        test_1(self)

        # -------------------------------------
        # ЗАГРУЗКА СПИСКОВ ДОСТУПА
        def test_2(self):
            print("WikiPermissions: " + test_2.__name__)
            wp = wp_test.WikiPermissions()
            stats = set()
            wp.create_permissions(13, 42)
            text = wp.get_xml_str()
            stats.add(wp.load_permissions(text))

            # wp.print_xml()

            if False in stats:
                self.__add_error("2", "Load permissions error")

        test_2(self)

        # -------------------------------------
        # ПРОВЕРКА ID
        def test_3(self):
            print("WikiPermissions: " + test_3.__name__)
            wp = wp_test.WikiPermissions()
            wp.create_permissions(42, 14)
            if wp.get_id() != 42:
                self.__add_error("3", "id error!")

        test_3(self)

        # -------------------------------------
        # ПРОВЕРКА ДОБАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯ В БЕЛЫЙ СПИСОК
        def test_4(self):
            print("WikiPermissions: " + test_4.__name__)
            stats = set()
            wp = wp_test.WikiPermissions()
            stats.add(wp.create_permissions(42, 14))
            stats.add(wp.add_to_white_list(1,"Vasya","watcher","None"))
            stats.add(wp.add_to_white_list(4,"Vasya","editor","None"))
            stats.add(not wp.add_to_white_list(4,"Vasya","ban","None"))
            stats.add(not wp.add_to_white_list(4,"Vasya","admin","None"))

            # wp.print_xml()
            if False in stats:
                self.__add_error("4", "add in white list error!")

        test_4(self)

        # -------------------------------------
        # ПРОВЕРКА ДОБАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯ В БЕЛЫЙ СПИСОК
        def test_5(self):
            print("WikiPermissions: " + test_5.__name__)
            stats = set()
            wp = wp_test.WikiPermissions()
            stats.add(wp.create_permissions(42, 14))
            stats.add(wp.add_to_black_list(1, "Vasya", "ban", "None"))
            stats.add(wp.add_to_black_list(4, "Vasya", "ban", "None"))
            stats.add(not wp.add_to_black_list(4, "Vasya", "wather", "None"))
            stats.add(not wp.add_to_black_list(4, "Vasya", "editor", "None"))

            # wp.print_xml()
            if False in stats:
                self.__add_error("5", "add in black list error!")

        test_5(self)

        # -------------------------------------
        # ПРОВЕРКА НА УДАОЕНИЕ ПОЛЬЗОВАТЕЛЯ ИЗ БЕЛОГО СПИСКА
        def test_6(self):
            print("WikiPermissions: " + test_6.__name__)
            stats = set()
            wp = wp_test.WikiPermissions()
            stats.add(wp.create_permissions(42, 14))
            stats.add(wp.add_to_white_list(1, "Vasya", "watcher", "None"))
            stats.add(wp.add_to_white_list(4, "Vasya", "watcher", "None"))
            stats.add(wp.remove_from_white_list(4))
            stats.add(not wp.remove_from_white_list(5))

            # wp.print_xml()
            if False in stats:
                self.__add_error("6", "remove in white list error!")

        test_6(self)

        # -------------------------------------
        # ПРОВЕРКА НА УДАОЕНИЕ ПОЛЬЗОВАТЕЛЯ ИЗ ЧЕРНОГО СПИСКА
        def test_7(self):
            print("WikiPermissions: " + test_7.__name__)
            stats = set()
            wp = wp_test.WikiPermissions()
            stats.add(wp.create_permissions(42, 14))
            stats.add(wp.add_to_black_list(1, "Vasya", "ban", "None"))
            stats.add(wp.add_to_black_list(4, "Vasya", "ban", "None"))
            stats.add(wp.remove_from_black_list(4))
            stats.add(not wp.remove_from_black_list(5))

            # wp.print_xml()
            if False in stats:
                self.__add_error("7", "remove in black list error!")

        test_7(self)

        # -------------------------------------
        # ПРОВЕРКА НА ПОЛУЧЕНИЕ КОРТЕЖА ПОЛЬЗОВАТЕЛЕЙ ИЗ БЕЛОГО СПИСКА
        def test_8(self):
            print("WikiPermissions: " + test_8.__name__)
            stats = set()
            wp = wp_test.WikiPermissions()
            stats.add(wp.create_permissions(42, 14))
            stats.add(wp.add_to_white_list(1, "Vasya", "watcher", "None"))
            stats.add(wp.add_to_white_list(4, "Vasya", "editor", "None"))
            users = wp.get_white_list()
            #print(users)
            if len(users) != 2 and users[0]["id"] != 1 and users[1]["permission"] != "editor":
                self.__add_error("8", "get tuple white error!")

            # wp.print_xml()
            if False in stats:
                self.__add_error("8", "get tuple in white list error!")

        test_8(self)

        # -------------------------------------
        # ПРОВЕРКА НА ПОЛУЧЕНИЕ КОРТЕЖА ПОЛЬЗОВАТЕЛЕЙ ИЗ БЕЛОГО СПИСКА
        def test_9(self):
            print("WikiPermissions: " + test_9.__name__)
            stats = set()
            wp = wp_test.WikiPermissions()
            stats.add(wp.create_permissions(42, 14))
            stats.add(wp.add_to_black_list(1, "Vasya", "ban", "None"))
            stats.add(wp.add_to_black_list(4, "Vasya", "ban", "None"))
            users = wp.get_black_list()
            # print(users)
            if len(users) != 2 and users[0]["id"] != 1 and users[1]["permission"] != "ban":
                self.__add_error("8", "get tuple black error!")

            # wp.print_xml()
            if False in stats:
                self.__add_error("9", "get tuple in black list error!")

        test_9(self)