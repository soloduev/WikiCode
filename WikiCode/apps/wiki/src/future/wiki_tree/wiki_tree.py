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


class WikiFileTree():
    """
    :VERSION: 0.02
    Класс для работы с файловым деревом на платформе WIKICODE.
    Файловое дерево педставляет из себя структуированный xml файл.
    Данный класс предоставляет удобное API, которое в зависимости от нужд пользователя, будет модернизировать его дерево.
    Также, дерево способно конвертировать xml в html код, под необходимый фронтенд.
    Дерево обязано содержать конфигурационный файл для создание фронтенд html файла, чтобы можно было удобно его настраивать.
    Исходный код дерева старается быть таким, чтобы деревао можно было легко модернизировать и улучшать, добавляя в него новые и новые элементы.
    В файле example_wiki_tree.xml отображен пример дерева и его возможностей.
    """

    def __init__(self):
        self.__xml_tree = None    # Сама XML строка
        pass

    # ---------------
    # Public methods:
    # ---------------

    # LOADS AND CREATING TREE

    def load_tree(self, xml_str: str) -> None:
        """Загружает дерево. Чтобы загрузить дерево в класс, передаем XML строку дерева"""
        self.__xml_tree = xml_str
        # Узнаем id дерева(оно совпадает с id пользователя владеющего этим деревом)

    def create_tree(self, id: int) -> bool:
        """Создает пустое дерево. Чтобы создать дерево, достаточно указать его id"""
        if type(id) == int:
            # Создаем новый корневой элемент
            wft_root = ET.Element('wiki_tree')
            # Задаем ему id
            wft_root.set('id',str(id))
            # Переводим xml в отформатированную строку
            self.__xml_tree = parseString(ET.tostring(wft_root)).toprettyxml()
            return True
        else:
            return False

    def is_valid(self) -> bool:
        """Проверка, валидно ли дерево. Выдает строку сообщения о валидности"""
        pass

    # GETS PARAMS TREE

    def get_id(self) -> int:
        """Возвращает id дерева"""
        pass

    def print_config(self) -> None:
        """Печатает параметры конфигурационного файла дерева"""
        pass

    def get_xml_str(self):
        return self.__xml_tree

    # WORK WITH FOLDERS

    def create_folder(self, id: int, name: str, access: str, type: str, style: str, show: str, id_folder: int = -1) -> None:
        """Создание новой папки"""
        pass

    def delete_folder(self, id: int) -> None:
        """Удаление папки с определенным id"""
        pass

    def rename_folder(self, id: int, new_name: str) -> None:
        """Переименование папки"""
        pass

    def reaccess_folder(self, id: int, new_access: str) -> None:
        """Изменение доступа папки"""
        pass

    def retype_folder(self, id: int, new_type: str) -> None:
        """Изменение типа папки"""
        pass

    def restyle_folder(self, id: int, new_style: str) -> None:
        """Изменение стиля папки"""
        pass

    def reshow_folder(self, id: int, new_show: str) -> None:
        """Изменение параметра отображения папки"""
        pass

    def move_folder(self, id: int, to_id: int) -> None:
        """Перемещение папки"""
        pass

    # WORK WITH PUBLICATIONS

    def create_publication(self, id: int, name: str, access: str, type: str, id_folder=-1) -> None:
        """Создание нового конспекта"""
        pass

    def delete_publication(self, id: int) -> None:
        """Удаление публикации"""

    def rename_publication(self, id: int, new_name: str) -> None:
        """Переименование публикации"""
        pass

    def reaccess_publication(self, id: int, new_access: str) -> None:
        """Изменение доступа конспекта"""
        pass

    def retype_publication(self, id: int, new_type: str) -> None:
        """Изменение типа конспекта"""
        pass

    def move_publication(self, id: int, to_id: int) -> None:
        """Перемещение конспекта. Если to_id == -1, то идет перемещение в корневую папку."""

    # VIEWS TREE

    def print_xml(self) -> None:
        """Выводит в консоль xml всего дерева"""
        if self.__xml_tree is not None:
            print(self.__xml_tree)

    def print_xml_folder(self, id: int) -> None:
        """Выводит xml папки"""
        pass

    def print_xml_publication(self, id: int) -> None:
        """Выводит xml конспекта"""
        pass

    def print(self) -> None:
        """Красиво выводит все дерево"""
        pass

    def print_folder(self, id: int) -> None:
        """Красиво выводит всю папку"""
        pass

    def print_publication(self, id: int) -> None:
        """Красиво выводт конспект"""
        pass

    # WORK WITH CONVERTING

    def to_html_dynamic(self) -> str:
        """Возвращает html динамического дерева, согласно конфигу"""
        pass

    def to_html_preview(self) -> str:
        """Возвращает html превью дерева, согласно конфигу"""
        pass

    # ----------------
    # Private methods:
    # ----------------











