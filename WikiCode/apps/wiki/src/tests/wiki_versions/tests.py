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

# ТЕСТИРОВАНИЕ ФУНКЦИОНАЛА WIKIVERSIONS

from WikiCode.apps.wiki.src.future.wiki_versions import wiki_versions as wv_test
import pickle

# Version:       0.012
# Total Tests:   12


class WikiVersionsTest(object):
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
        # Создание версий
        def test_1(self):
            print("WikiVersions: " + test_1.__name__)
            wv = wv_test.WikiVersions()
            stats = set()

            if False in stats:
                self.__add_error("1", "Create versions error")

        test_1(self)

        # -------------------------------------
        # Тестирование функции нахождения наибольшей общей последовательности
        def test_2(self):
            print("WikiVersions: " + test_2.__name__)
            wv = wv_test.WikiVersions()

            seq_1 = ["a", "b", "c", "d", "1", "0", "3", "a", "b"]
            seq_2 = ["x", "d", "3", "a", "b", "a", "c", "k"]
            true_answer = ['d', '3', 'a', 'b']
            result = wv._WikiVersions__highest_overall_sequence(seq_1, seq_2)
            if true_answer != result: self.__add_error("2", "highest_overall_sequence(seq_1, seq_2)")

        test_2(self)

        # -------------------------------------
        # Тестирование функции возвращения разницы двух последовательностей
        def test_3(self):
            print("WikiVersions: " + test_3.__name__)
            wv = wv_test.WikiVersions()

            need_result = (((0, 'a'), (1, 'b'), (2, 'c'), (4, '1'), (5, '0')), ((0, 'x'), (5, 'a'), (6, 'c'), (7, 'k')))

            seq_1 = ["a", "b", "c", "d", "1", "0", "3", "a", "b"]
            seq_2 = ["x", "d", "3", "a", "b", "a", "c", "k"]
            result = wv._WikiVersions__get_diff(seq_1, seq_2)
            if need_result != result: self.__add_error("3", "get_diff(seq_1, seq_2)")

        test_3(self)

        # -------------------------------------
        # Тестирование создания новой версии и архива
        def test_4(self):
            print("WikiVersions: " + test_4.__name__)
            wv = wv_test.WikiVersions()

            wv.create_versions(1, ["Hello", "world!", "I", "love", "you!"])
            obj = wv.get_archive()
            need = {'graph': {1: []}, 'versions': {1: {'type': 'HeadLeaf', 'branch': 'master', 'seq': ['Hello', 'world!', 'I', 'love', 'you!'], 'comments': [], 'date': '', 'id_user': 1, 'commit_msg': '', 'diff': []}}, 'head_index': 1}
            if need != pickle.loads(obj):
                self.__add_error("4", "get_archive()")

        test_4(self)

        # -------------------------------------
        # Тестирование загрузки архива
        def test_5(self):
            print("WikiVersions: " + test_5.__name__)

            wv = wv_test.WikiVersions()
            wv.create_versions(1, ["Hello", "world!", "I", "love", "you!"])
            some_archive = wv.get_archive()

            wv_2 = wv_test.WikiVersions()
            wv_2.load_versions(some_archive)
            obj = wv_2.get_archive()
            need = {'graph': {1: []}, 'versions': {1: {'type': 'HeadLeaf', 'branch': 'master', 'seq': ['Hello', 'world!', 'I', 'love', 'you!'], 'comments': [], 'date': '', 'id_user': 1, 'commit_msg': '', 'diff': []}}, 'head_index': 1}
            if need != pickle.loads(obj):
                self.__add_error("5", "load_versions()")

        test_5(self)

        # -------------------------------------
        # Тестирование получения head_index
        def test_6(self):
            print("WikiVersions: " + test_6.__name__)

            wv = wv_test.WikiVersions()

            if wv.get_head_index() is not None:
                self.__add_error("6", "get_head_index()")

            wv.create_versions(1, ["Hello", "world!", "I", "love", "you!"])

            if wv.get_head_index() != 1:
                self.__add_error("6", "get_head_index()")

        test_6(self)

        # -------------------------------------
        # Тестирование создания новой версии.(Новая версия всегда создается после head версии)
        def test_7(self):
            print("WikiVersions: " + test_7.__name__)

            wv = wv_test.WikiVersions()
            if wv.new_version(1, ["Hi", "world!", "We", "love", "me!", "Bye!"]) != False:
                self.__add_error("7", "new_version()")

            wv.create_versions(1, ["Hello", "world!", "I", "love", "you!"])
            wv.new_version(1, ["Hi", "world!", "We", "love", "me!", "Bye!"])
            # wv.show_tree()
            if wv.get_head_index() != 1:
                self.__add_error("7", "get_head_index()")

            need = {'date': '', 'commit_msg': '', 'type': 'Head', 'id_user': 1, 'branch': 'master', 'comments': [], 'seq': ['Hello', 'world!', 'I', 'love', 'you!'], 'diff': []}
            if wv.get_dict_head() != need:
                self.__add_error("7", "get_dict_head()")

            need = {'seq': ['Hello', 'world!', 'I', 'love', 'you!'], 'type': 'Head', 'comments': [], 'branch': 'master', 'diff': [], 'commit_msg': '', 'id_user': 1, 'date': ''}
            if wv.get_dict_version(1) != need:
                self.__add_error("7", "get_dict_version(1)")

            need = {'branch': 'unknown', 'comments': [], 'type': 'Leaf', 'date': '', 'diff': (((0, 'Hello'), (2, 'I'), (4, 'you!')), ((0, 'Hi'), (2, 'We'), (4, 'me!'), (5, 'Bye!'))), 'seq': None, 'id_user': 1, 'commit_msg': ''}
            if wv.get_dict_version(2) != need:
                self.__add_error("7", "get_dict_version(2)")

            wv.new_version(1, ["Hi", "world!", "I", "love", "you!"])
            wv.new_version(1, ["Hi", "world!", "I", "love", "we!"])
            # wv.show_tree()

            need = {'seq': None, 'comments': [], 'type': 'Leaf', 'branch': 'unknown', 'diff': (((0, 'Hello'), (4, 'you!')), ((0, 'Hi'), (4, 'we!'))), 'date': '', 'id_user': 1, 'commit_msg': ''}
            if wv.get_dict_version(4) != need:
                self.__add_error("7", "get_dict_version(4)")

        test_7(self)

        # -------------------------------------
        # Тестирование накатов версий
        def test_8(self):
            print("WikiVersions: " + test_8.__name__)

            wv = wv_test.WikiVersions()

            result = wv._WikiVersions__to_roll(["Hello", "world!", "I", "love", "you!"],
                                      (((0, 'Hello'), (2, 'I'), (4, 'you!')),
                                       ((0, 'Hi'), (2, 'We'), (4, 'me!'), (5, 'Bye!'))))

            need = ['Hi', 'world!', 'We', 'love', 'me!', 'Bye!']
            if result[0] != need:
                self.__add_error("8", "_WikiVersions__to_roll() - 1")
            need = (((0, 'Hi'), (2, 'We'), (4, 'me!'), (5, 'Bye!')), ((0, 'Hello'), (2, 'I'), (4, 'you!')))
            if result[1] != need:
                self.__add_error("8", "_WikiVersions__to_roll() - 1.1")


            result = wv._WikiVersions__to_roll(["Hello", "world!", "I", "love", "you!"],
                                               (((4, 'you!'),),
                                                ((0, 'Perfect!'), (1, 'This is best SVC!'), (5, 'very'), (7, 'we!'))))

            need = ['Perfect!', 'This is best SVC!', 'Hello', 'world!', 'I', 'very', 'love', 'we!']
            if result[0] != need:
                self.__add_error("8", "_WikiVersions__to_roll() - 2")
            need = (((0, 'Perfect!'), (1, 'This is best SVC!'), (5, 'very'), (7, 'we!')), ((4, 'you!'),))
            if result[1] != need:
                self.__add_error("8", "_WikiVersions__to_roll() - 2.1")


            result = wv._WikiVersions__to_roll(["Hello", "world!", "I", "love", "you!"],
                                               (((0, 'Hi'), (1, 'world!'), (2, 'I'), (3, 'love'), (4, 'you!')), ()))

            need = []
            if result[0] != need:
                self.__add_error("8", "_WikiVersions__to_roll() - 3")
            need = ((), ((0, 'Hello'), (1, 'world!'), (2, 'I'), (3, 'love'), (4, 'you!')))
            if result[1] != need:
                self.__add_error("8", "_WikiVersions__to_roll() - 3.1")

            result = wv._WikiVersions__to_roll(["Hello", "world!", "I", "love", "you!"],
                                               (((0, 'Hi'), (1, 'world!'), (2, 'I'), (3, 'love'), (4, 'you!')),
                                                ((0, 'My'), (1, 'name'), (2, 'is'), (3, 'Charls'), (4, 'Darvin'))))

            need = ['My', 'name', 'is', 'Charls', 'Darvin']
            if result[0] != need:
                self.__add_error("8", "_WikiVersions__to_roll() - 4")
            need = (((0, 'My'), (1, 'name'), (2, 'is'), (3, 'Charls'), (4, 'Darvin')), ((0, 'Hello'), (1, 'world!'), (2, 'I'), (3, 'love'), (4, 'you!')))
            if result[1] != need:
                self.__add_error("8", "_WikiVersions__to_roll() - 4.1")


            result = wv._WikiVersions__to_roll([],
                                               ((), ((0, 'My'), (1, 'name'), (2, 'is'), (3, 'Charls'), (4, 'Darvin'))))

            need = ['My', 'name', 'is', 'Charls', 'Darvin']
            if result[0] != need:
                self.__add_error("8", "_WikiVersions__to_roll() - 5")
            need = (((0, 'My'), (1, 'name'), (2, 'is'), (3, 'Charls'), (4, 'Darvin')), ())
            if result[1] != need:
                self.__add_error("8", "_WikiVersions__to_roll() - 4.1")

        test_8(self)

        # -------------------------------------
        # Тестирование накатов, чисто для Node, Head, Leaf. Все без мержей.
        def test_9(self):
            print("WikiVersions: " + test_9.__name__)

            # Варианты версий:
            ver_1 = ['Perfect!', 'This is best SVC!', 'Hello', 'world!', 'I', 'very', 'love', 'we!']
            ver_2 = ["Hello", "world!", "I", "love", "you!"]
            ver_3 = ["Hello", "world!", "I", "love", "me!"]
            ver_4 = ["Some text...", "And", "love", "we!"]
            ver_5 = ["Append", "Some text...", "Or", "love", "we", "all!"]
            ver_6 = ["love"]

            wv = wv_test.WikiVersions()
            wv.create_versions(1, ver_1)
            wv.new_version(1, ver_2)
            wv.set_head(2)
            wv.new_version(1, ver_3)
            wv.set_head(3)
            if wv.get_raw_tree() != '1:Node -> 2, 2:Node -> 1, 2:Node -> 3, 3:HeadLeaf -> 2, ':
                self.__add_error("9", "set_head() - 1")
            if wv.get_dict_head()['seq'] != ver_3:
                self.__add_error("9", "set_head() - 1.1")
            wv.set_head(1)
            if wv.get_raw_tree() != '1:Head -> 2, 2:Node -> 1, 2:Node -> 3, 3:Leaf -> 2, ':
                self.__add_error("9", "set_head() - 2")
            if wv.get_dict_head()['seq'] != ver_1:
                self.__add_error("9", "set_head() - 2.1")
            wv.set_head(2)
            if wv.get_raw_tree() != '1:Node -> 2, 2:Head -> 1, 2:Head -> 3, 3:Leaf -> 2, ':
                self.__add_error("9", "set_head() - 3")
            if wv.get_dict_head()['seq'] != ver_2:
                self.__add_error("9", "set_head() - 3.1")
            wv.set_head(1)
            wv.new_version(1, ver_4)
            if wv.get_raw_tree() != '1:Head -> 2, 1:Head -> 4, 2:Node -> 1, 2:Node -> 3, 3:Leaf -> 2, 4:Leaf -> 1, ':
                self.__add_error("9", "set_head() - 4")
            wv.set_head(4)
            if wv.get_raw_tree() != '1:Node -> 2, 1:Node -> 4, 2:Node -> 1, 2:Node -> 3, 3:Leaf -> 2, 4:HeadLeaf -> 1, ':
                self.__add_error("9", "set_head() - 5")
            if wv.get_dict_head()['seq'] != ver_4:
                self.__add_error("9", "set_head() - 5.1")
            wv.new_version(1, ver_5)
            if wv.get_raw_tree() != '1:Node -> 2, 1:Node -> 4, 2:Node -> 1, 2:Node -> 3, 3:Leaf -> 2, 4:Head -> 1, 4:Head -> 5, 5:Leaf -> 4, ':
                self.__add_error("9", "set_head() - 6")
            if wv.get_dict_head()['seq'] != ver_4:
                self.__add_error("9", "set_head() - 6.1")
            wv.new_version(1, ver_6)
            if wv.get_raw_tree() != '1:Node -> 2, 1:Node -> 4, 2:Node -> 1, 2:Node -> 3, 3:Leaf -> 2, 4:Head -> 1, 4:Head -> 5, 4:Head -> 6, 5:Leaf -> 4, 6:Leaf -> 4, ':
                self.__add_error("9", "set_head() - 7")
            if wv.get_dict_head()['seq'] != ver_4:
                self.__add_error("9", "set_head() - 7.1")
            wv.set_head(6)
            if wv.get_raw_tree() != '1:Node -> 2, 1:Node -> 4, 2:Node -> 1, 2:Node -> 3, 3:Leaf -> 2, 4:Node -> 1, 4:Node -> 5, 4:Node -> 6, 5:Leaf -> 4, 6:HeadLeaf -> 4, ':
                self.__add_error("9", "set_head() - 8")
            if wv.get_dict_head()['seq'] != ver_6:
                self.__add_error("9", "set_head() - 8.1")
            wv.set_head(5)
            if wv.get_raw_tree() != '1:Node -> 2, 1:Node -> 4, 2:Node -> 1, 2:Node -> 3, 3:Leaf -> 2, 4:Node -> 1, 4:Node -> 5, 4:Node -> 6, 5:HeadLeaf -> 4, 6:Leaf -> 4, ':
                self.__add_error("9", "set_head() - 9")
            if wv.get_dict_head()['seq'] != ver_5:
                self.__add_error("9", "set_head() - 9.1")
            wv.set_head(2)
            if wv.get_raw_tree() != '1:Node -> 2, 1:Node -> 4, 2:Head -> 1, 2:Head -> 3, 3:Leaf -> 2, 4:Node -> 1, 4:Node -> 5, 4:Node -> 6, 5:Leaf -> 4, 6:Leaf -> 4, ':
                self.__add_error("9", "set_head() - 10")
            if wv.get_dict_head()['seq'] != ver_2:
                self.__add_error("9", "set_head() - 10.1")
            wv.set_head(6)
            if wv.get_raw_tree() != '1:Node -> 2, 1:Node -> 4, 2:Node -> 1, 2:Node -> 3, 3:Leaf -> 2, 4:Node -> 1, 4:Node -> 5, 4:Node -> 6, 5:Leaf -> 4, 6:HeadLeaf -> 4, ':
                self.__add_error("9", "set_head() - 11")
            if wv.get_dict_head()['seq'] != ver_6:
                self.__add_error("9", "set_head() - 11.1")
            wv.set_head(3)
            if wv.get_raw_tree() != '1:Node -> 2, 1:Node -> 4, 2:Node -> 1, 2:Node -> 3, 3:HeadLeaf -> 2, 4:Node -> 1, 4:Node -> 5, 4:Node -> 6, 5:Leaf -> 4, 6:Leaf -> 4, ':
                self.__add_error("9", "set_head() - 12")
            if wv.get_dict_head()['seq'] != ver_3:
                self.__add_error("9", "set_head() - 12.1")
            wv.set_head(3)
            if wv.get_raw_tree() != '1:Node -> 2, 1:Node -> 4, 2:Node -> 1, 2:Node -> 3, 3:HeadLeaf -> 2, 4:Node -> 1, 4:Node -> 5, 4:Node -> 6, 5:Leaf -> 4, 6:Leaf -> 4, ':
                self.__add_error("9", "set_head() - 13")
            if wv.get_dict_head()['seq'] != ver_3:
                self.__add_error("9", "set_head() - 13.1")
            wv.set_head(1)
            if wv.get_raw_tree() != '1:Head -> 2, 1:Head -> 4, 2:Node -> 1, 2:Node -> 3, 3:Leaf -> 2, 4:Node -> 1, 4:Node -> 5, 4:Node -> 6, 5:Leaf -> 4, 6:Leaf -> 4, ':
                self.__add_error("9", "set_head() - 13")
            if wv.get_dict_head()['seq'] != ver_1:
                self.__add_error("9", "set_head() - 13.1")

        test_9(self)

        # -------------------------------------
        # Тестирование установки комментариев
        def test_10(self):
            print("WikiVersions: " + test_10.__name__)

            wv = wv_test.WikiVersions()
            wv.create_versions(1, ["Hello", "world!", "I", "love", "you!"])
            wv.new_version(1, ["Hello", "world!", "I", "love", "me!"])
            wv.set_head(2)
            wv.new_version(1, ["Hi", "world!", "I", "love", "me!"])
            wv.set_head(3)
            wv.new_version(1, ["Hi", "planet!", "I", "love", "me!"])
            wv.set_head(4)

            wv.set_comment(2, "Edit you to me")
            wv.set_comment(2, "Really!")

            if wv.get_dict_version(2)['comments'] != ['Edit you to me', 'Really!']:
                self.__add_error("10", "set_comments() - 1")
            if wv.get_dict_version(3)['comments']:
                self.__add_error("10", "set_comments() - 2")

            wv.set_comment(4, "Wow!")
            if wv.get_dict_version(4)['comments'] != ['Wow!']:
                self.__add_error("10", "set_comments() - 3")

        test_10(self)

        # -------------------------------------
        # Тестирование получения seq любой версии. То есть, получения, любой версии
        def test_11(self):
            print("WikiVersions: " + test_11.__name__)

            wv = wv_test.WikiVersions()
            wv.create_versions(1, ["Hello", "world!", "I", "love", "you!"])
            wv.new_version(1, ["Hello", "world!", "I", "love", "me!"])
            wv.set_head(2)
            wv.new_version(1, ["Hi", "world!", "I", "love", "me!"])
            wv.set_head(3)
            wv.new_version(1, ["Hi", "planet!", "I", "love", "me!"])
            wv.set_head(1)
            wv.new_version(1, ["What", "is", "me!", "a"])
            wv.set_head(5)
            wv.new_version(1, ["What", "me!", "a", "!"])
            wv.set_head(6)

            if wv.get_version(1) != ["Hello", "world!", "I", "love", "you!"]:
                self.__add_error("11", "get_version(1)")
            if wv.get_version(5) != ["What", "is", "me!", "a"]:
                self.__add_error("11", "get_version(5)")
            if wv.get_version(2) != ["Hello", "world!", "I", "love", "me!"]:
                self.__add_error("11", "get_version(2)")
            if wv.get_version(4) != ["Hi", "planet!", "I", "love", "me!"]:
                self.__add_error("11", "get_version(4)")
            if wv.get_version(6) != ["What", "me!", "a", "!"]:
                self.__add_error("11", "get_version(6)")
            if wv.get_version(5) != ["What", "is", "me!", "a"]:
                self.__add_error("11", "get_version(5)")

        test_11(self)

        # -------------------------------------
        # Тестирование получения head версии
        def test_12(self):
            print("WikiVersions: " + test_12.__name__)

            wv = wv_test.WikiVersions()
            wv.create_versions(1, ["Hello", "world!", "I", "love", "you!"])
            wv.new_version(1, ["Hello", "world!", "I", "love", "me!"])
            wv.set_head(2)
            wv.new_version(1, ["Hi", "world!", "I", "love", "me!"])
            wv.set_head(3)
            wv.new_version(1, ["Hi", "planet!", "I", "love", "me!"])
            wv.set_head(1)
            wv.new_version(1, ["What", "is", "me!", "a"])
            wv.set_head(5)
            wv.new_version(1, ["What", "me!", "a", "!"])
            wv.set_head(6)

            if wv.get_head() != ["What", "me!", "a", "!"]:
                self.__add_error("12", "get_head() - 1")

            wv.set_head(1)

            if wv.get_head() != ["Hello", "world!", "I", "love", "you!"]:
                self.__add_error("12", "get_head() - 2")

            wv.set_head(4)

            if wv.get_head() != ["Hi", "planet!", "I", "love", "me!"]:
                self.__add_error("12", "get_head() - 3")

        test_12(self)

