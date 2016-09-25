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

from WikiCode.apps.wiki.src.modules.wiki_tree.config import params as CONFIG


class WikiFileTree():
    """
    :VERSION: 0.26
    Класс для работы с файловым деревом на платформе WIKICODE.
    Файловое дерево педставляет из себя структуированный xml файл.
    Данный класс предоставляет удобное API, которое в зависимости от нужд пользователя, будет модернизировать его дерево.
    Также, дерево способно конвертировать xml в html код, под необходимый фронтенд.
    Дерево обязано содержать конфигурационный файл для создание фронтенд html файла, чтобы можно было удобно его настраивать.
    Исходный код дерева старается быть таким, чтобы деревао можно было легко модернизировать и улучшать, добавляя в него новые и новые элементы.
    В файле example.xml отображен пример дерева и его возможностей.
    """

    def __init__(self):
        self.__xml_tree = None    # Сама XML строка

    # ---------------
    # Public methods:
    # ---------------

    # LOADS AND CREATING TREE

    def load_tree(self, xml_str: str) -> None:
        """Загружает дерево. Чтобы загрузить дерево в класс, передаем XML строку дерева"""
        if type(xml_str) == str:
            self.__xml_tree = xml_str
        else:
            self.__xml_tree = None
        # Узнаем id дерева(оно совпадает с id пользователя владеющего этим деревом)

    def create_tree(self, id: int) -> bool:
        """Создает пустое дерево. Чтобы создать дерево, достаточно указать его id"""
        if type(id) == int:
            # Создаем новый корневой элемент
            wft_root = ET.Element('wiki_tree')
            # Задаем ему id
            wft_root.set('id',str(id))
            # Переводим xml в строку
            self.__xml_tree = ET.tostring(wft_root)
            return True
        else:
            self.__xml_tree = None
            return False

    # GETS PARAMS TREE

    def get_id(self) -> int:
        """Возвращает id дерева"""
        if self.__xml_tree is not None:
            root = ET.fromstring(self.__xml_tree)
            tree_id = int(root.get('id'))
            return tree_id
        else:
            return None

    def print_config(self) -> None:
        """Печатает параметры конфигурационного файла дерева"""
        for key in CONFIG:
            print(key, ":", CONFIG[key])

    def get_xml_str(self):
        result_str = self.__format_xml(self.__xml_tree)
        result_str = result_str.replace('\n', '')
        result_str = result_str.replace('\t', '')
        result_str = result_str.replace('>', '>\n')
        return result_str

    def get_num_root_folders(self) -> int:
        """Возвращает количество корневых папок"""
        if self.__xml_tree is not None:
            root = ET.fromstring(self.__xml_tree)
            return len(root.findall("./folder"))
        else:
            return None

    # WORK WITH FOLDERS

    def create_folder(self, id: int, name: str, access: str, type: str, style: str, view: str, id_folder: int = -1) -> bool:
        """Создание новой папки"""
        if self.__xml_tree:
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)

            # Создание корня для папки
            new_folder = ET.Element('folder')

            # Проверяем параметры на валидность
            if not self.__check_name(name): return False        # Праверяем имя на валидность
            # Проверяем наличие папки с таким же именем
            # some code here ... (Пока думаю, делать ли это)
            # Проверяем, не отрицательный ли id
            if not self.__check_id(id): return False
            if not self.__check_access(access): return False    # Проверяем, правильное ли значение доступа задается папке
            if not self.__check_type(type): return False        # Проверяем, правильный ли тип задается папке
            if not self.__check_style(style): return False      # Проверяем, правильный ли стиль задается папке
            if not self.__check_view(view): return False        # Проверяем, правильный ли вид задается папке

            # Создаем параметры новой папки
            # Создавая новое имя папки, очищаем его от пробелов в начале и в конце
            new_folder.set('name', self.__erase_str_side_all(name, " "))
            new_folder.set('id', str(id))
            new_folder.set('access', access)
            new_folder.set('type', type)
            new_folder.set('style', style)
            new_folder.set('view', view)

            # Узнаем, в какой папке создавать новую папку
            # Если в корне
            if id_folder == -1:
                root.append(new_folder)
            # Если в другой папке
            else:
                # Проход по элементам в поисках нужного id
                for folder in root.iter('folder'):
                    if folder.get('id') == str(id_folder):
                        # Проверяем родительский доступ в папке:
                        if folder.get('access') == 'private':
                            new_folder.set('access','private')
                        folder.append(new_folder)
                        break

            self.__xml_tree = ET.tostring(root)
            return True
        else:
            return False

    # TODO: ВАЖНО! ПОТОМ ДОБАВИТЬ, ЧТО ПОСЛЕ УДАЛЕНИЯ ПАПКИ, ВОЗВРАЩАЮТСЯ ID ВСЕХ СОДЕРЖАЩИХСЯ ПАПОК И КОНСПЕКТОВ
    # TODO: СЕЙЧАС ПРОСТО УДАЛЯЮТСЯ ТОЛЬКО ПАПКИ, Т.К. ПОКА НЕТ ВОЗМОЖНОСТИ СОЗДАВАТЬ КОНСПЕКТЫ
    def delete_folder(self, id_folder: int) -> bool:
        """Удаление папки с определенным id"""
        if self.__xml_tree is not None:
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            parent = root.find('.//folder[@id="'+str(id_folder)+'"]...')
            if parent is not None:
                folder = parent.find('./folder[@id="'+str(id_folder)+'"]')
                if folder is not None:
                    parent.remove(folder)
                    self.__xml_tree = ET.tostring(root)
                    return True
            return False
        else:
            return False

    def rename_folder(self, id_folder: int, new_name: str) -> bool:
        """Переименование папки"""
        if self.__xml_tree is not None and type(new_name) == str:
            # Проверяем новое имя на валидность
            if not self.__check_name(new_name): return False
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            for folder in root.iter('folder'):
                if folder.get('id') == str(id_folder):
                    folder.set('name', self.__erase_str_side_all(new_name, " "))
                    self.__xml_tree = ET.tostring(root)
                    return True
            return False

    def reaccess_folder(self, id_folder: int, new_access: str) -> bool:
        """Изменение доступа папки"""
        if self.__xml_tree is not None and type(new_access) == str:
            # Проверяем новый доступ на валидность
            if not self.__check_access(new_access): return False
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            for folder in root.iter('folder'):
                if folder.get('id') == str(id_folder):
                    parent = root.find('.//folder[@id="' + str(id_folder) + '"]...')
                    # Если родительская папка имела приватный доступ, то изменить доступ на публичный невозможно
                    if parent.get('access') == 'private':
                        folder.set('access', 'private')

                    else:
                        # Если меняем доступ у папки на приватный, меняем все подпапки на приватные
                        if new_access == 'private':
                            for sub_folder in folder.iter('folder'):
                                sub_folder.set('access', 'private')
                        folder.set('access', new_access)
                    self.__xml_tree = ET.tostring(root)
                    return True
            return False

    def retype_folder(self, id_folder: int, new_type: str) -> bool:
        """Изменение типа папки"""
        if self.__xml_tree is not None and type(new_type) == str:
            # Проверяем новый тип на валидность
            if not self.__check_type(new_type): return False
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            for folder in root.iter('folder'):
                if folder.get('id') == str(id_folder):
                    folder.set('type', new_type)
                    self.__xml_tree = ET.tostring(root)
                    return True
            return False

    def restyle_folder(self, id_folder: int, new_style: str) -> bool:
        """Изменение стиля папки"""
        if self.__xml_tree is not None and type(new_style) == str:
            # Проверяем новый стиль на валидность
            if not self.__check_style(new_style): return False
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            for folder in root.iter('folder'):
                if folder.get('id') == str(id_folder):
                    folder.set('style', new_style)
                    self.__xml_tree = ET.tostring(root)
                    return True
            return False

    def review_folder(self, id_folder: int, new_show: str) -> bool:
        """Изменение параметра отображения папки"""
        if self.__xml_tree is not None and type(new_show) == str:
            # Проверяем новый вид на валидность
            if not self.__check_view(new_show): return False
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            for folder in root.iter('folder'):
                if folder.get('id') == str(id_folder):
                    folder.set('style', new_show)
                    self.__xml_tree = ET.tostring(root)
                    return True
            return False

    # ВАЖНО! При перемещении папки, помимо, ее перемещения, необходимо еще наследовать доступ, если например публичная папка попала в приватную
    def move_folder(self, id: int, to_id: int) -> bool:
        """Перемещение папки"""
        pass

    # WORK WITH PUBLICATIONS

    def create_publication(self, id: int, name: str, access: str, type: str, id_folder=-1) -> bool:
        """Создание нового конспекта"""
        if self.__xml_tree is not None:
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)

            # Создание корня для конспека
            new_publication = ET.Element('publication')

            # Проверяем параметры на валидность
            if not self.__check_publication_name(name): return False  # Праверяем имя на валидность
            # Проверяем наличие папки с таким же именем
            # some code here ... (Пока думаю, делать ли это)
            # Проверяем, не отрицательный ли id
            if not self.__check_id(id): return False
            if not self.__check_access(access): return False  # Проверяем, правильное ли значение доступа задается папке
            if not self.__check_type(type): return False  # Проверяем, правильный ли тип задается папке

            # Создаем параметры нового конспекта
            # Новое имя папки очищаем от пробелов в начале и в конце
            new_publication.set('name', self.__erase_str_side_all(name, " "))
            new_publication.set('id', str(id))
            new_publication.set('access', access)
            new_publication.set('type', type)

            # Узнаем, в какой папке создавать новую папку
            # Если в корне
            if id_folder == -1:
                root.append(new_publication)
            # Если в другой папке
            else:
                # Проход по элементам в поисках нужного id
                for folder in root.iter('folder'):
                    if folder.get('id') == str(id_folder):
                        # Если создаем конспект в приватной папке, он автоматически становится приватным
                        if folder.get('access') == 'private':
                            new_publication.set('access', 'private')
                        folder.append(new_publication)
                        break

            self.__xml_tree = ET.tostring(root)
            return True
        else:
            return False

    def delete_publication(self, id_publication: int) -> bool:
        """Удаление публикации"""
        if self.__xml_tree is not None:
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            parent = root.find('.//publication[@id="' + str(id_publication) + '"]...')
            if parent is not None:
                publication = parent.find('./publication[@id="' + str(id_publication) + '"]')
                if publication is not None:
                    parent.remove(publication)
                    self.__xml_tree = ET.tostring(root)
                    return True
                return False
            else:
                return False

    def rename_publication(self, id_publication: int, new_name: str) -> bool:
        """Переименование публикации"""
        if self.__xml_tree is not None and type(new_name) == str:
            # Проверяем новое имя на валидность
            if not self.__check_publication_name(new_name): return False
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            for publication in root.iter('publication'):
                if publication.get('id') == str(id_publication):
                    publication.set('name', self.__erase_str_side_all(new_name, " "))
                    self.__xml_tree = ET.tostring(root)
                    return True
            return False

    def reaccess_publication(self, id_publication: int, new_access: str) -> bool:
        """Изменение доступа конспекта"""
        if self.__xml_tree is not None and type(new_access) == str:
            # Проверяем новый доступ на валидность
            if not self.__check_access(new_access): return False
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            for publication in root.iter('publication'):
                if publication.get('id') == str(id_publication):
                    # Получаем родителя
                    parent = root.find('.//publication[@id="' + str(id_publication) + '"]...')
                    # Если доступ родителя приватный, то публикация остается приватной
                    if parent.get('access') == 'private':
                        publication.set('access', 'private')
                    else:
                        publication.set('access', new_access)
                    self.__xml_tree = ET.tostring(root)
                    return True
            return False

    def retype_publication(self, id_publication: int, new_type: str) -> bool:
        """Изменение типа конспекта"""
        if self.__xml_tree is not None and type(new_type) == str:
            # Проверяем новый тип на валидность
            if not self.__check_type(new_type): return False
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            for publication in root.iter('publication'):
                if publication.get('id') == str(id_publication):
                    publication.set('type', new_type)
                    self.__xml_tree = ET.tostring(root)
                    return True
            return False

    def move_publication(self, id_publication: int, to_id_folder: int) -> bool:
        """Перемещение конспекта. Если to_id == -1, то идет перемещение в корневую папку."""
        if self.__xml_tree is not None and type(id_publication) == int and type(to_id_folder) == int:
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            publication_moved = None
            parent_1 = root.find('.//publication[@id="' + str(id_publication) + '"]...')
            if parent_1 is not None:
                publication_1 = parent_1.find('./publication[@id="' + str(id_publication) + '"]')
                if publication_1 is not None:
                    publication_moved = publication_1
                    parent_1.remove(publication_1)
                else:
                    return False
            else:
                return False

            if publication_moved is not None:
                if to_id_folder == -1:
                    root.append(publication_moved)
                    self.__xml_tree = ET.tostring(root)
                    return True
                else:
                    parent_2 = root.find('.//folder[@id="' + str(to_id_folder) + '"]...')
                    if parent_2 is not None:
                        folder = parent_2.find('./folder[@id="' + str(to_id_folder) + '"]')
                        if folder is not None:
                            if folder.get('access') == "private":
                                publication_moved.set('access','private')
                            folder.append(publication_moved)
                            self.__xml_tree = ET.tostring(root)
                            return True
                        else:
                            return False
                    else:
                        return False
            else:
                return False
        else:
            return False

    # VIEWS TREE

    def print_xml(self) -> None:
        """Выводит в консоль xml всего дерева"""
        if self.__xml_tree is not None:
            print(self.__format_xml(self.__xml_tree))

    # TODO: Реализовать. Может, когда-нибудь пригодится для отладки
    def print_xml_folder(self, id: int) -> None:
        """Выводит xml папки"""
        pass

    # TODO: Реализовать. Может, когда-нибудь пригодится для отладки
    def print_xml_publication(self, id: int) -> None:
        """Выводит xml конспекта"""
        pass

    # TODO: Реализовать. Может, когда-нибудь пригодится для отладки
    def print(self) -> None:
        """Красиво выводит все дерево"""
        pass

    # TODO: Реализовать. Может, когда-нибудь пригодится для отладки
    def print_folder(self, id: int) -> None:
        """Красиво выводит всю папку"""
        pass

    # TODO: Реализовать. Может, когда-нибудь пригодится для отладки
    def print_publication(self, id: int) -> None:
        """Красиво выводт конспект"""
        pass

    # WORK WITH CONVERTING

    # Variant 1
    def to_html_dynamic(self) -> str:
        """Возвращает html динамического дерева"""
        if self.__xml_tree is not None:
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            # Получаем все папки в корне и проходим по ним
            folders = root.findall("./folder")
            root = ET.Element("root")
            for folder in folders:
                # Вызываем рекурсивный метод обработки папки
                self.__append_dynamic_folder(folder, root)

            # Форматируем xml в строку
            result_str = self.__format_xml(ET.tostring(root))
            # Убираем xml decloration
            result_str = result_str.replace('<?xml version="1.0" ?>\n', '')
            # Убираем корневой вспомагательный элемент
            result_str = result_str.replace('<root>\n', '')
            result_str = result_str.replace('</root>\n', '')

            return result_str
        else:
            return ""

    # Variant 1
    def to_html_dynamic_folders(self) -> str:
        """Возвращает html динамического дерева только с папками"""
        if self.__xml_tree is not None:
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            # Получаем все папки в корне и проходим по ним
            folders = root.findall("./folder")
            root = ET.Element("root")
            for folder in folders:
                # Вызываем рекурсивный метод обработки папки
                self.__append_dynamic_folder_without_publs(folder, root)

            # Форматируем xml в строку
            result_str = self.__format_xml(ET.tostring(root))
            # Убираем xml decloration
            result_str = result_str.replace('<?xml version="1.0" ?>\n', '')
            # Убираем корневой вспомагательный элемент
            result_str = result_str.replace('<root>\n', '')
            result_str = result_str.replace('</root>\n', '')

            return result_str
        else:
            return ""

    # Variant 1
    def to_html_preview(self) -> str:
        """Возвращает html превью дерева"""
        if self.__xml_tree is not None:
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_tree)
            # Получаем все папки в корне и проходим по ним
            folders = root.findall("./folder")
            root = ET.Element("root")
            for folder in folders:
                # Вызываем рекурсивный метод обработки папки
                self.__append_folder(folder, root)

            # Форматируем xml в строку
            result_str = self.__format_xml(ET.tostring(root))
            # Убираем xml decloration
            result_str = result_str.replace('<?xml version="1.0" ?>\n', '')
            # Убираем корневой вспомагательный элемент
            result_str = result_str.replace('<root>\n', '')
            result_str = result_str.replace('</root>\n', '')

            return result_str
        else:
            return ""

    # WORK WITH ELEMENTS

    def sort_element(self, id_folder):
        """Сортирует все элементы в указанной папке"""
        pass

    # ----------------
    # Private methods:
    # ----------------

    def __format_xml(self, xml_str):
        """Выравнивание xml строки"""
        return parseString(xml_str).toprettyxml()

    def __check_name(self, name: str) -> bool:
        """Проверяем новое название папки на запрещенные символы"""
        # Очищаем пробелы по бокам и смотрим, не пустая ли строка
        if self.__erase_str_side_all(name, " ") == "": return False
        if name == "": return False
        for symbol in CONFIG["DSFF"]:
            if name.find(symbol) != -1:
                return False
        return True

    def __check_publication_name(self, name: str) -> bool:
        """Проверяем новое название конспекта на запрещенные символы"""
        # Очищаем пробелы по бокам и смотрим, не пустая ли строка
        if self.__erase_str_side_all(name, " ") == "": return False
        if name == "": return False
        for symbol in CONFIG["DSFP"]:
            if name.find(symbol) != -1:
                return False
        return True

    def __check_id(self, id: int) -> bool:
        """Проверяем id на валидность"""
        if id < -1:
            return False
        else:
            return True

    def __check_access(self, access: str) -> bool:
        """Проверяем access на валидность"""
        if access not in CONFIG["FAV"]:
            return False
        else:
            return True

    def __check_type(self, type: str) -> bool:
        if type not in CONFIG["FTV"]:
            return False
        else:
            return True

    def __check_style(self, style: str) -> bool:
        if style not in CONFIG["FSV"]:
            return False
        else:
            return True

    def __check_view(self, view: str) -> bool:
        if view not in CONFIG["FVV"]:
            return False
        else:
            return True

    def __erase_str_side(self, str, symbols):
        """Очищает указанную строку по бокам один раз"""
        if str[:len(symbols)] == symbols:
            str = str[len(symbols):]
        if str[-len(symbols):] == symbols:
            str = str[:-len(symbols)]
        return str

    def __erase_str_side_all(self, str, symbols):
        """Очищает указанную строку по бокам, до тех пор, пока она не исчезнет"""
        isErased = True
        while isErased:
            isErased = False
            if str[:len(symbols)] == symbols:
                str = str[len(symbols):]
                isErased = True
            if str[-len(symbols):] == symbols:
                str = str[:-len(symbols)]
                isErased = True
        return str

    # Variant 1
    def __append_folder(self, folder, root):
        """Добавляет папку в нод"""
        li = ET.Element("li")
        li_href = ET.Element("a")
        li_href.set('href', '#')
        li_href.text = folder.get('name')
        li.append(li_href)
        ul = ET.Element("ul")
        ul.text = " "
        li.append(ul)
        root.append(li)
        folders = folder.findall("./folder")
        for child_folder in folders:
            self.__append_folder(child_folder, ul)
        publications = folder.findall("./publication")
        for publication in publications:
            publ_li = ET.Element('li')
            publ_li.text = publication.get('name')
            publ_href = ET.Element('a')
            publ_href.set('href', '/page/' + str(publication.get('id')))
            publ_href.set('class', 'btn btn-xs btn-link')
            publ_span = ET.Element('span')
            publ_span.set('class', 'glyphicon glyphicon-share-alt')
            publ_href.append(publ_span)
            publ_li.append(publ_href)
            ul.append(publ_li)

    # Variant 1
    def __append_dynamic_folder(self, folder, root):
        """Добавляет папку в нод"""
        li = ET.Element("li")
        li.set('type_elem', 'folder')
        li.set('class', 'task')
        li.set('data-id', 'folder:' + folder.get('id'))
        li.set('id', 'folder:' + folder.get('id'))
        li.set('data-jstree', '{ "type" : "folder" }')
        li.text = folder.get('name')
        ul = ET.Element("ul")
        ul.text = " "
        li.append(ul)
        root.append(li)
        folders = folder.findall("./folder")
        for child_folder in folders:
            self.__append_dynamic_folder(child_folder, ul)
        publications = folder.findall("./publication")
        for publication in publications:
            publ_li = ET.Element('li')
            publ_li.set('type_elem', 'publ')
            publ_li.set('class', 'task')
            publ_li.set('data-id', 'publ:' + publication.get('id'))
            publ_li.set('id', 'publ:' + publication.get('id'))
            publ_li.set('data-jstree', '{ "type" : "publ" }')
            publ_li.text = publication.get('name')
            ul.append(publ_li)

    # Variant 1

    def __append_dynamic_folder_without_publs(self, folder, root):
        """Добавляет папку в нод"""
        li = ET.Element("li")
        li.set('type_elem', 'folder')
        li.set('class', 'task')
        li.set('data-id', 'folder:' + folder.get('id'))
        li.set('id', 'folder:' + folder.get('id'))
        li.set('data-jstree', '{ "type" : "folder" }')
        li.text = folder.get('name')
        ul = ET.Element("ul")
        ul.text = " "
        li.append(ul)
        root.append(li)
        folders = folder.findall("./folder")
        for child_folder in folders:
            self.__append_dynamic_folder_without_publs(child_folder, ul)










