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
from WikiCode.apps.wiki.src.future.wiki_comments.config import params as CONFIG


class WikiComments():
    """
       :VERSION: 0.5
       Класс для работы с комментариями на платформе WIKICODE.
       Комментарии педставляет из себя структуированный xml файл.
       Данный класс предоставляет удобное API, которое в зависимости от нужд пользователя, будет модернизировать его дерево.
       Также, этот класс способен конвертировать xml в html код, под необходимый фронтенд.
       Класс работы с комментариями обязан содержать конфигурационный файл для создание фронтенд html файла, чтобы можно было удобно его настраивать.
       Исходный код класса комментариев старается быть таким, чтобы комментарии можно было легко модернизировать и улучшать, добавляя в него новые и новые элементы.
       В файле example.xml отображен пример xml комментарев и их возможностей.
       """
    def __init__(self):
        self.__xml_comments = None

    # ---------------
    # Public methods:
    # ---------------

    # LOADS AND CREATING TREE

    def load_comments(self, xml_str: str) -> None:
        """Загрузка комментариев. Необхожимо передать xml строчку."""
        if type(xml_str) == str:
            self.__xml_comments = xml_str
        else:
            self.__xml_comments = None

    def create_comments(self, id: int) -> bool:
        """Создает пустую xml комментариев. Необходимо передать id новых комментариев."""
        if type(id) == int:
            # Создаем новый корневой элемент
            wc_root = ET.Element('wiki_comments')
            # Задаем ему id
            wc_root.set('id', str(id))
            # Переводим xml в строку
            self.__xml_comments = ET.tostring(wc_root)
            return True
        else:
            self.__xml_comments = None
            return False

    # GETS PARAMS TREE

    def get_id(self) -> int:
        """Возвращает id комментариев"""
        if self.__xml_comments is not None:
            root = ET.fromstring(self.__xml_comments)
            comments_id = int(root.get('id'))
            return comments_id
        else:
            return None

    def print_config(self) -> None:
        """Печатает параметры конфигурационного файла комментариев"""
        for key in CONFIG:
            print(key, ":", CONFIG[key])

    def get_xml_str(self) -> str:
        """Возвращает xml строку текущих комментариев"""
        return self.__format_xml(self.__xml_comments)

    # WORK WITH COMMENTS

    def create_comment(self, id_comment: int ,user_id: int, text: str, user_name: str,
                       date: str, is_moderator: bool) -> bool:
        """Создает новый комментарий в дереве."""
        if self.__xml_comments:
            # Получаем корневой элемент текущих комментариев
            root = ET.fromstring(self.__xml_comments)
            # Создание корня для комментария
            new_comment = ET.Element('comment')
            # Задаем параметры новому комментарию
            new_comment.set('id_comment', str(id_comment))
            new_comment.set('user_id', str(user_id))
            new_comment.set('text', text)
            new_comment.set('user_name', user_name)
            new_comment.set('date', date)
            new_comment.set('is_moderator', str(is_moderator))
            # Параметры, которые задаем по-умолчанию для только что созданного комментария
            new_comment.set('answered_id', str(None))
            new_comment.set('answered_name', str(None))
            new_comment.set('rating', str(0))
            new_comment.set('is_edit', str(False))
            new_comment.set('is_claim', str(False))
            # Добавляем новый комментарий в корень
            root.append(new_comment)
            # Сохраняем комментарии ввиде строки
            self.__xml_comments = ET.tostring(root)
            return True
        else:
            return False


    def edit_comment(self, id_comment: int, text: str, date: str) -> bool:
        """Позволяет редактировать комментарий, если не прошло определенное время указанное в конфигурационном файле."""
        pass


    def delete_comment(self, id_comment: int) -> bool:
        """Удаляет комментарий, указав его id."""
        pass


    def reply(self, new_id:int, reply_id: int, text: str, reply_name: int,
              date: str, is_moderator: bool) -> bool:
        """Ответ на существующий комментарий"""
        pass

    def complain(self, id_comment: int) -> bool:
        """Отправить жалобу на комментарий."""
        pass

    def up_rating(self, id_comment: int) -> bool:
        """Повысить рейтинг комментарию"""
        pass

    def down_rating(self, id_comment: int) -> bool:
        """Понизить рейтинг комментарию"""
        pass

    # VIEWS TREE

    def print_comment(self, id_comment: int) -> None:
        """Отображает информацию о комментарии"""
        pass

    def debug_comment(self, id_comment: int) -> tuple:
        """Возвращает все параметры комментария в виде кортежа. Необходимо для тестирования."""
        pass

    def print(self) -> None:
        """Отображает красиво все комментарии"""
        pass

    def print_xml(self) -> None:
        """Отображает отформатировнную xml строку текущих комментариев."""
        if self.__xml_comments is not None:
            print(self.__format_xml(self.__xml_comments))

    # WORK WITH CONVERTING

    def to_html(self) -> str:
        """Конвертурует по конфигурационному файлу html фронтенд для комментариев."""
        pass

    # ----------------
    # Private methods:
    # ----------------

    def __format_xml(self, xml_str):
        """Выравнивание xml строки"""
        return parseString(xml_str).toprettyxml()

