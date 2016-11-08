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


class WikiVersions:
    """
       :VERSION: 0.16
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
                "type": 'HeadLeaf',
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

    def new_version(self, id_user: int, new_seq: list, message: str = "", date: str = ""):
        """Создает новую версию для head.
        Принимает обновленную последовательность, id пользователя, который произвел
        новую версию, и сообщение к коммиту"""
        if self.__graph:
            new_version_index = len(self.__versions) + 1
            self.__append_version(self.__graph,
                                  self.get_head_index(),
                                  new_version_index)

            head_version = self.__versions[self.__head_index]
            diff = self.__get_diff(head_version['seq'], new_seq)

            # Определяем тип Head, чтобы заменить его на новый, если Head является листом
            new_head_type = head_version['type']
            if new_head_type == 'HeadLeaf':
                new_head_type = "Head"
            elif new_head_type == 'HeadMergeLeaf':
                new_head_type = "HeadMerge"

            # Заменяем тип head
            head_version['type'] = new_head_type

            self.__versions[new_version_index] = {
                "id_user": id_user,
                "commit_msg": message,
                "comments": [],
                "diff": diff,
                "date": date,
                "type": 'Leaf',
                "seq": None,
                "branch": 'unknown',  # TODO: Реализовать получение имени ветки от head
            }

            return True
        else:
            return False

    def set_head(self, num_version: int):
        """Устанавливает head любой из версий.
        То есть, производит откаты и накаты и меняет основной файл."""
        if self.__graph:
            # Сначала получаем путь от head версии, до той, на которую необходимо переключиться
            path = self.__find_shortest_path(self.__graph, self.__head_index, num_version)

            # Затем переходим от одной версии к другой по циклу
            for i in range(0, len(path) - 1):
                next_ver = self.__versions[path[i + 1]]
                self.__switch_versions([path[i + 1], next_ver['type']])

            return True
        else:
            return False

    def set_comment(self, num_version: int, comment: str):
        """Добавляет комментарий к любой из версий"""
        if self.__graph:
            if 0 < num_version <= len(self.__graph):
                self.__versions[num_version]['comments'].append(comment)
        else:
            return False

    def get_version(self, num_version: int):
        """Возвращает определенную версию.
        То есть, делает откаты, накаты но не меняет файл.
        Возвращает md файл(seq)"""
        if self.__graph:
            if 0 < num_version <= len(self.__graph):
                # Запоминаем индекс текущей head версии
                head_index = self.__head_index

                # Получаем head нужной версии
                self.set_head(num_version)

                # Затем, получаем seq head версии
                result_seq = self.__versions[self.__head_index]['seq']

                # И возвращаем обратно head версию
                self.set_head(head_index)

                return result_seq
            else:
                return False
        else:
            return False

    def merge(self, versions: list):
        """Производит объединение любых версий в одну.
        Что делать в случае конфликтов, необходимо указать в конфиге."""
        pass

    def get_head(self):
        """Возвращает последовательность HEAD версии"""
        if self.__graph:
            return self.__versions[self.__head_index]['seq']
        else:
            return False

    def get_diff(self, version: int):
        """Возвращает в виде кортежа разницу между предыдущей версией(относительно расположения head версии)"""
        if self.__graph:
            if 0 < version <= len(self.__graph) and version != self.__head_index:
                return self.__versions[version]['diff']
            else:
                return False
        else:
            return False

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
        self.__print_graph(self.__graph)

    def get_dict_tree(self):
        """Возвращает self.__graph"""
        return self.__graph

    def show_version(self, num_version: int):
        """Отображает краткую информацию о версии под номером"""
        print(self.__versions[num_version])

    def get_dict_version(self, num_version: int):
        """Возвращает определенную версию в виде словаря"""
        return self.__versions[num_version]

    def show_head(self):
        """Отображает краткую информацию о head версии"""
        print(self.__versions[self.__head_index])

    def get_dict_head(self):
        """Возвращает head версию в виде словаря"""
        return self.__versions[self.__head_index]

    def show_dif(self, version: int):
        """Отображает разницу между предыдущей версией"""
        pass

    def get_head_index(self) -> int:
        return self.__head_index

    def get_raw_tree(self):
        result_raw = ""
        if self.__graph:
            for key, values in self.__graph.items():
                if not values:
                    result_raw += str(key) + ":" + str(self.__versions[key]['type'])
                for v in values:
                    result_raw += str(key) + ":" + str(self.__versions[key]['type']) + " -> " + str(v) + ", "
            return result_raw
        else:
            return None

    # GENERATING

    def generate_js(self):
        """ Метод генерирует js код для отрисовки ветки версий """
        result_js = ""
        if self.__graph:
            # Сначала находим все листы
            leafs = []
            for key, value in self.__versions.items():
                if "Leaf" in value["type"]:
                    leafs.append(key)
            # Затем, зная все листы, получаем все ветки(путь для каждой)
            branches = []
            for leaf in leafs:
                branches.append(self.__find_shortest_path(self.__graph, 1, leaf))
            # Создаем все js переменные для веток
            for i in range(0, len(branches)):
                result_js += 'var branch_' + str(i + 1) + ' = gitgraph.branch("branch_' + str(i + 1) + '");\n'
            # Производим коммиты
            visited_versions = set()
            str_commits = []
            for i in range(0, len(branches)):
                for j in range(0, len(branches[i])):
                    if branches[i][j] not in visited_versions:
                        visited_versions.add(branches[i][j])
                        if j == 0:
                            if self.__head_index == branches[i][j]:
                                str_commits.append(('branch_' + str(i + 1) + '.commit({message: "Head", dotColor: "white"});\n', branches[i][j]))
                            else:
                                str_commits.append(('branch_' + str(i + 1) + '.commit({message: " "});\n', branches[i][j]))
                        else:
                            for isc in range(0, len(str_commits)):
                                if str_commits[isc][1] == branches[i][j-1]:
                                    if self.__head_index == branches[i][j]:
                                        str_commits.insert(isc+1, ('branch_' + str(i + 1) + '.commit({message: " ", dotColor: "white"});\n', branches[i][j]))
                                    else:
                                        str_commits.insert(isc+1, ('branch_' + str(i + 1) + '.commit({message: " "});\n', branches[i][j]))
            # Добавляем коммиты в результирующую строку
            for sc in str_commits:
                result_js += sc[0]

        return result_js

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
                res += [seq_1[i]]
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

    def __switch_versions(self, next_ver):
        """Данный метод переключает РЯДОМ стоящие версии.
        Аргумент next_ver представляет из себя пару: индекс версии и тип версии, на которую необходимо переключить
        head версию.
        Например: [31, "Merge"]. """
        if self.__graph:
            head = self.__versions[self.__head_index]
            head_type = head['type']
            to_index = next_ver[0]
            to_type = next_ver[1]
            to_version = self.__versions[to_index]

            if head_type == 'Head':
                if to_type == 'Node':
                    roll = self.__to_roll(head['seq'], to_version['diff'])
                    to_version['type'] = 'Head'
                    to_version['diff'] = []
                    to_version['seq'] = roll[0]
                    head['type'] = 'Node'
                    head['diff'] = roll[1]
                    head['seq'] = None
                    self.__head_index = to_index
                elif to_type == 'Leaf':
                    roll = self.__to_roll(head['seq'], to_version['diff'])
                    to_version['type'] = 'HeadLeaf'
                    to_version['diff'] = []
                    to_version['seq'] = roll[0]
                    head['type'] = 'Node'
                    head['diff'] = roll[1]
                    head['seq'] = None
                    self.__head_index = to_index
                elif to_type == 'Merge':
                    pass
                elif to_type == 'MergeLeaf':
                    pass
                else:
                    return False
            elif head_type == 'HeadLeaf':
                if to_type == 'Node':
                    roll = self.__to_roll(head['seq'], to_version['diff'])
                    to_version['type'] = 'Head'
                    to_version['diff'] = []
                    to_version['seq'] = roll[0]
                    head['type'] = 'Leaf'
                    head['diff'] = roll[1]
                    head['seq'] = None
                    self.__head_index = to_index
                elif to_type == 'Merge':
                    pass
                else:
                    return False
            elif head_type == 'HeadMerge':
                if to_type == 'Node':
                    pass
                elif to_type == 'Leaf':
                    pass
                elif to_type == 'Merge':
                    pass
                elif to_type == 'MergeLeaf':
                    pass
                else:
                    return False
            elif head_type == 'HeadMergeLeaf':
                if to_type == 'Node':
                    pass
                elif to_type == 'Merge':
                    pass
                else:
                    return False
            else:
                return False
        else:
            return False

    def __to_roll(self, seq, diff):
        """Производить накат версии.
        Возвращает кортеж.
        Первый параметр кортежа - новая последовательность seq.
        Второй парметр кортежа, это новый порожденный diff."""

        # Порождаем новую последовательность, проходим по всем удалениям, и удаляем части
        new_seq = seq.copy()
        offset = 0
        for item in diff[0]:
            index = item[0]
            value = item[1]
            del new_seq[index - offset]
            offset += 1

        # Теперь, добавляем новые
        for item in diff[1]:
            index = item[0]
            value = item[1]
            new_seq.insert(index, value)

        new_diff = self.__get_diff(new_seq, seq)

        return new_seq, new_diff

    # WORK WITH GRAPH
    # Все методы ниже, работают чисто на уровне переменной self.__graph

    # Нахождение наикротчайшего пути
    def __find_shortest_path(self, graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not start in graph:
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = self.__find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    # Вывод всего графа для отладки
    def __print_graph(self, graph):
        if self.__graph:
            for key, values in graph.items():
                if not values:
                    print(str(key) + ":" + str(self.__versions[key]['type']))
                for v in values:
                    print(str(key) + ":" + str(self.__versions[key]['type']) + " -> " + str(v))
        else:
            print("Tree not found!")

    # Добавление новой версии в граф
    def __append_version(self, graph, prev, new):
        graph[prev].append(new)
        graph[new] = [prev]

    # Проверяет, является ли версия листом
    def __is_leaf(self, graph, version):
        links = graph[version]
        if len(graph) == 1:
            return True
        elif version != 1 and len(links) == 1:
            return True
        else:
            return False

    # Слияние версий
    def __merge_versions(self, graph, versions, new):
        # Сначала проверяем все версии, являются ли они листами
        is_leafs = True
        for version in versions:
            if not self.__is_leaf(graph, version):
                is_leafs = False
                break
        if is_leafs:
            graph[new] = []
            for version in versions:
                graph[version].append(new)
                graph[new].append(version)
            return True
        else:
            return False
