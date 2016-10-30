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

import pickle
from WikiCode.apps.wiki.src.future.wiki_versions import config as CONFIG


class WikiVersions:
    """
       :VERSION: 0.7
       Система контроля версий для md конспектов.
       Жует только md конспекты и собственный архив с версиями.
       Архив представляет из себя обычный сериализованный python файл, в котором хранится вся информация о текущей
       версии и всех изменениях.

       Класс хранит все версии в виде разниц между файлами.
       В виде целого файла, хранит лишь текущую его версию.
       """

    def __init__(self):
        self.__graph = None
        self.__versions = None
        self.__head_index = None

    # ---------------
    # Public methods:
    # ---------------

    # LOADS AND CREATING

    def create_versions(self, id_user: int, seq: list, comment: str = "", commit_msg: str = "", date: str = ""):
        """Принимает id конспекта и его md текст. Создает файл первой версии. То есть, сам файл."""
        self.__graph = {1: []}
        self.__versions = {
            1: {
                "id_user": id_user,
                "commit_msg": commit_msg,
                "comments": [],
                "diff": [],
                "date": date,
                "type": 'Head',
                "seq": seq,
                "branch": 'master',
            }
        }
        self.__head_index = 1


    def get_archive(self):
        """Возвращает архив всех версий."""
        if self.__head_index:
            data = {
                "head_index": self.__head_index,
                "versions": self.__versions,
                "graph": self.__graph
            }
            # Сериализуем данные в архив
            archive = pickle.dumps(data)
            return archive
        else:
            return None

    def load_versions(self, archive):
        """Загружает архив и собственно, сам head, то есть, главный файл."""
        try:
            data = pickle.loads(archive)
            self.__head_index = data["head_index"]
            self.__versions = data["versions"]
            self.__graph = data["graph"]
        except TypeError:
            print("WikiVersions can't load archive")

    # WORK WITH VERSIONS

    def new_version(self, new_seq: list, id_user: int, message: str = None):
        """Создает новую версию для head.
        Принимает обновленную последовательность, id пользователя, который произвел
        новую версию, и сообщение к коммиту"""



    def set_head(self, num_version: int):
        """Устанавливает head любой из версий.
        То есть, производит откаты и накаты и меняет основной файл."""


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
        """Возвращает последовательность HEAD версии"""


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


    def show_dif(self, version: int):
        """Отображает разницу между предыдущей версией"""
        pass

    def get_head_index(self) -> int:
        pass

    # GENERATING

    # ----------------
    # Private methods:
    # ----------------

    def __highest_overall_sequence(self, seq_1, seq_2):
        """Функция нахождения наибольшей общей последовательности. Может принимать только последовательности,
        элементы которых можно друг с другом сравнивать и те последовательности, к которым можно добавлять элементы
        с помощью оператора '+=', и те последовательности, к которым можно обратиться по индексу 'seq[i]'."""

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
                    max_len[i][j] = 1 + max_len[i + 1][j + 1]
                else:
                    max_len[i][j] = max(max_len[i + 1][j], max_len[i][j + 1])

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
                if max_len[i][j] == max_len[i + 1][j]:
                    i += 1
                else:
                    j += 1

        return res

    def __get_diff(self, seq_1, seq_2):
        """Возвращает кортеж изменений. 0: Сначала удаления, 1: Затем добавления.
        Каждое изменение содержит:
        0: Индекс в последовательности
        1: Содержимое изменения
        Принимает последовательность до и новую последовательность."""

        # Получаем наибольшую общую последовательность
        hos = self.__highest_overall_sequence(seq_1, seq_2)
        len_hos = len(hos)

        res_diff = []
        for i in range(0, len(seq_1) + len(seq_2)):
            res_diff.append(None)

        # Сначала получаем порядок последовательность удалений и того, что осталось
        seq_del = []
        hos_index = 0
        for i in range(0, len(seq_1)):
            if hos_index < len_hos:
                if seq_1[i] == hos[hos_index]:
                    hos_index += 1
                    continue
            seq_del.append((i, seq_1[i]))

        # Затем, получаем порядок того, что добавилось
        seq_add = []
        hos_index = 0
        for i in range(0, len(seq_2)):
            if hos_index < len_hos:
                if seq_2[i] == hos[hos_index]:
                    hos_index += 1
                    continue
            seq_add.append((i, seq_2[i]))

        return tuple(seq_del), tuple(seq_add)