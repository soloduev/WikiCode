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


class WikiPermissions():
    """
       :VERSION: 0.1
       Класс для работы со списками доступа у конспекта.
       Список доступа педставляет из себя структуированный xml файл.
       Данный класс предоставляет удобное API, которое в зависимости от нужд пользователя, будет модернизировать его дерево.
       Также, этот класс способен конвертировать xml в необходимые структуры данных для клиентской части.
       Исходный код класса списка доступов старается быть таким, чтобы его можно было легко модернизировать и улучшать, добавляя в него новые и новые элементы.
       В файле example.xml отображен пример xml списка и его возможностей.
       """
    def __init__(self):
        self.__xml_ermissions = None

    # ---------------
    # Public methods:
    # ---------------

    # LOADS AND CREATING TREE

    def load_permissions(self, xml_str: str) -> None:
        """Загрузка списка. Необхожимо передать xml строчку."""
        pass

    def create_permissions(self, id: int) -> bool:
        """Создает пустую xml списка. Необходимо передать id нового списка."""
        pass

    # GETS PARAMS TREE

    def get_id(self) -> int:
        """Возвращает id списка"""
        pass

    def get_xml_str(self) -> str:
        """Возвращает xml строку текущего списка доступа"""
        pass

    # WORK WITH LIST

    def add_to_white_list(self, id_user: int, name_user: str, permission: str, status: str):
        """Добавление пользователя в белый список"""
        pass

    def add_to_black_list(self, id_user: int, name_user: str, permission: str, status: str):
        """Добавление пользователя в черный список"""
        pass

    def remove_from_white_list(self, id_user):
        """Убрать пользователя из белого списка"""
        pass

    def remove_from_black_list(self, id_user):
        """Убрать пользователя из черного списка"""
        pass

    def get_white_list(self):
        """Вернуть кортеж всех пользователей, из белого списка"""
        pass

    def get_black_list(self):
        """Вернуть кортеж всех пользователей, из белого списка"""
        pass

    def show(self):
        """Напечатать все списки доступа"""
        pass

    # ----------------
    # Private methods:
    # ----------------

    def __format_xml(self, xml_str):
        """Выравнивание xml строки"""
        return parseString(xml_str).toprettyxml()

