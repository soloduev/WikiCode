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

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from WikiCode.apps.wiki.src.future.wiki_versions import config as CONFIG


class WikiVersions():
    """
       :VERSION: 0.2
       Система контроля версий для md конспектов.
       Жует только md конспекты и собственный архив с версиями.
       Архив представляет из себя обычный zip/tar файл, в котором перечислены текстовые файлы версий,
       а также, единая папка с файлами, которые отличаются от md конспектов.

       Класс хранит все версии в виде разниц между файлами.
       В виде целого файла, хранит лишь текущую его версию.
       """
    def __init__(self):
        pass

    # ---------------
    # Inner classes
    # ---------------

    # Отдельная версия
    class Version():
        def __init__(self):
            self.__id = 0
            self.__comment = ""
            self.__commit_msg = ""
            self.__diff = []
            # Формат хранения разницы с предыдущей/следующей версией:
            # Каждый элемент списка представляет из себя кортеж, именуемый операцией
            # Порядок операций применяется к файлу сверху вниз
            # Первый параметр операции - это тип:
            # "+" - добавлена строка в файле
            # "-" - убрана строка в файле
            # Второй параметр - это индекс строки. В случае с добавлением, индекс указывает, на какое место нужно
            #    добавить новую строку. В случае с удалением, все понятно.
            # При выполнении операций, все строки файла нумеруются с нуля.
            # При добавлении и удалении изменяется переменная смещения. Например, если произошло 5 раз удаление,
            #    то смещение будет равно -5. Это необходимо для того, чтобы сравнивались нужные индексы строк до
            #    и после.
            # Сама версия, ничего не знает о самом файле.

        def set_id(self, id):
            self.__id = id

        def set_comment(self, comment):
            self.__comment = comment

        def set_commit_msg(self, msg):
            self.__commit_msg = msg

        def append_diff(self, type, index):
            pass

        




    # ---------------
    # Public methods:
    # ---------------

    # LOADS AND CREATING

    def create_versions(self, id_publication: int, md_str: str):
        """Принимает id конспекта и его md текст. Создает файл первой версии. То есть, сам файл."""
        pass

    def get_archive(self):
        """Возвращает архив всех версий."""
        pass

    def save(self, path: str):
        """Сохраняет архив по определнному пути"""
        pass

    def load_versions(self, archive):
        """Загружает архив и собственно, сам head, то есть, главный файл."""
        pass

    def load(self, path_to_archive):
        """Загружает архив по его пути."""
        pass

    # WORK WITH VERSIONS

    def new_version(self, md_str: str, comments: list, message: str = None):
        """Создает новую версию для head.
        Принимает обновленный md text и список комментариев к абзацам.
        Возвращает новый список комментариев, для их обновления в БД."""
        pass

    def set_head(self, num_version: int):
        """Устанавливает head любой из версий.
        То есть, производит откаты и накаты и меняет основной файл.
        Возвращает новый список комментариев, для их обновления в БД."""
        pass

    def set_comment(self, num_version: int, comment: int):
        """Добавляет комментарий к любой из версий"""
        pass

    def get_version(self, num_version: int):
        """Возвращает определенную версию.
        То есть, делает откаты, накаты но не меняет файл.
        Возвращает md файл и список комментариев, для получения их в БД."""
        pass

    def merge(self, versions: list):
        """Производит объединение любых версий в одну.
        Что делать в случае конфликтов, необходимо указать в конфиге."""
        pass

    def get_head(self):
        """Возвращает md файл."""
        pass

    def get_diff(self, version: int):
        """Возвращает в виде списка разницу между предыдущей версией"""
        pass

    def get_diff_head(self):
        """Возвращает в виде списка разницу между предыдущей head версией"""
        pass

    def edit_commit_message(self, version: int, new_message: str):
        """Изменяет сообщение определенного коммита"""
        pass

    def delete_version(self, version: int):
        """Удалит версию, если она не head и не ниже head"""
        pass

    # VIEWS VERSIONS

    def show_history(self):
        """Отображает историю изменений."""
        pass

    def show_tree(self):
        """Отображает красиво отформатированную строку ветки для дебага."""
        pass

    def show_version(self, num_version: int):
        """Отображает краткую информацию о версии под номером"""
        pass

    def show_head(self):
        """Отображает краткую информацию о head версии"""
        pass

    def show_dif(self, version: int):
        """Отображает разницу между предыдущей версией"""
        pass

    # GENERATING

    # ----------------
    # Private methods:
    # ----------------
    def __highest_overall_sequence(self, seq_1, seq_2):
        """Функция нахождения наибольшей общей последовательности"""

        # Сначала составляем пустую матрицу, заполняем ее нулями. N seq_1 + 1 and N seq_2 + 1.
        max_len = []
        for i in range(0, len(seq_1) + 1):
            max_len.append([])
            for j in range(0, len(seq_2) + 1):
                max_len[i].append(0)

        # Проходим по матрице и заполняем ее в соответствии с алгоритмов
        for i in range(len(seq_1) - 1, -1, -1):
            for j in range(len(seq_2) - 1, -1, -1):
                if seq_1[i] == seq_2[j]:
                    max_len[i][j] = 1 + max_len[i+1][j+1]
                else:
                    max_len[i][j] = max(max_len[i+1][j], max_len[i][j+1])

        # Создаем пустую результирующую последовательность
        type_seq = type(seq_1)
        res = type_seq()

        # Проходим по матрице сверху вниз, оперативно получая максимальную последовательность.
        i = 0
        j = 0
        while max_len[i][j] != 0 and i < len(seq_1) and j < len(seq_2):
            if seq_1[i] == seq_2[j]:
                res += seq_1[i]
                i += 1
                j += 1
            else:
                if max_len[i][j] == max_len[i+1][j]:
                    i += 1
                else:
                    j += 1

        return res
