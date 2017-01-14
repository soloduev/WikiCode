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

from WikiCode.apps.wiki.src.modules.wiki_comments.config import params as CONFIG


class WikiComments():
    """
       :VERSION: 0.18
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
        result_str = self.__format_xml(self.__xml_comments)
        result_str = result_str.replace('\n', '')
        result_str = result_str.replace('\t', '')
        result_str = result_str.replace('>', '>\n')
        return result_str

    # WORK WITH COMMENTS
    # TODO: Необходимо добавить валидацию полей, особенно дату
    def create_comment(self, id_comment: int ,user_id: int, text: str, user_name: str,
                       date: str, is_moderator: bool) -> bool:
        """Создает новый комментарий в дереве."""
        if self.__xml_comments:
            # Получаем корневой элемент текущих комментариев
            root = ET.fromstring(self.__xml_comments)
            # Создание корня для комментария
            new_comment = ET.Element('comment')
            # Задаем параметры новому комментарию
            new_comment.set('id', str(id_comment))
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

    # TODO: Произвести валидацию текста по конфигу
    # TODO: Произвести валидацию даты по конфигу
    # TODO: Сделать так, чтобы нельзя было изменить комментарий из-за разницы дат. Опять же согласно конфигу.
    def edit_comment(self, id_comment: int, text: str, date: str) -> bool:
        """Позволяет редактировать комментарий, если не прошло определенное время указанное в конфигурационном файле."""
        if self.__xml_comments:
            # Получаем корневой элемент текущих комментариев
            root = ET.fromstring(self.__xml_comments)
            # Получаем необходимый нам комментарий по его id
            for comment in root.iter('comment'):
                if comment.get('id') == str(id_comment):
                    # Меняем его текст и дату и ставим флаг, что комментарий был изменен
                    comment.set('text', text)
                    comment.set('date', date)
                    comment.set('is_edit', str(True))
                    # Сохраняем все
                    self.__xml_comments = ET.tostring(root)
                    return True
            return False
        else:
            return False


    def delete_comment(self, id_comment: int) -> bool:
        """Удаляет комментарий, указав его id."""
        if self.__xml_comments is not None:
            # Получаем корневой элемент текущего дерева
            root = ET.fromstring(self.__xml_comments)
            parent = root.find('.//comment[@id="' + str(id_comment) + '"]...')
            if parent is not None:
                comment = parent.find('./comment[@id="' + str(id_comment) + '"]')
                if comment is not None:
                    parent.remove(comment)
                    self.__xml_comments = ET.tostring(root)
                    return True
            return False
        else:
            return False

    # TODO: Произвести валидацию всех аргументов
    def reply(self, new_id:int, user_id: int, user_name: str, text: str, reply_id: int,
              date: str, is_moderator: bool) -> bool:
        """Ответ на существующий комментарий"""
        if self.__xml_comments:
            # Получаем корневой элемент текущих комментариев
            root = ET.fromstring(self.__xml_comments)
            # Получаем необходимый нам комментарий по его id
            for comment in root.iter('comment'):
                if comment.get('id') == str(reply_id):
                    # Создаем ответ
                    new_comment = ET.Element('comment')
                    # Задаем параметры новому комментарию
                    new_comment.set('id', str(new_id))
                    new_comment.set('user_id', str(user_id))
                    new_comment.set('text', text)
                    new_comment.set('user_name', user_name)
                    new_comment.set('date', date)
                    new_comment.set('is_moderator', str(is_moderator))
                    # Параметры, которые задаем по-умолчанию для только что созданного комментария
                    new_comment.set('answered_id', str(reply_id))
                    new_comment.set('answered_name', comment.get('user_name'))
                    new_comment.set('rating', str(0))
                    new_comment.set('is_edit', str(False))
                    new_comment.set('is_claim', str(False))
                    # Сохраняем все
                    comment.append(new_comment)
                    self.__xml_comments = ET.tostring(root)
                    return True
            return False
        else:
            return False

    def complain(self, id_comment: int) -> bool:
        """Отправить жалобу на комментарий."""
        if self.__xml_comments:
            # Получаем корневой элемент текущих комментариев
            root = ET.fromstring(self.__xml_comments)
            # Получаем необходимый нам комментарий по его id
            for comment in root.iter('comment'):
                if comment.get('id') == str(id_comment):
                    # Меняем флаг
                    comment.set('is_claim', str(True))
                    # Сохраняем все
                    self.__xml_comments = ET.tostring(root)
                    return True
            return False
        else:
            return False

    def up_rating(self, id_comment: int) -> bool:
        """Повысить рейтинг комментарию"""
        if self.__xml_comments:
            # Получаем корневой элемент текущих комментариев
            root = ET.fromstring(self.__xml_comments)
            # Получаем необходимый нам комментарий по его id
            for comment in root.iter('comment'):
                if comment.get('id') == str(id_comment):
                    # Меняем рейтинг
                    comment.set('rating', str(int(comment.get('rating')) + 1))
                    # Сохраняем все
                    self.__xml_comments = ET.tostring(root)
                    return True
            return False
        else:
            return False

    def down_rating(self, id_comment: int) -> bool:
        """Понизить рейтинг комментарию"""
        if self.__xml_comments:
            # Получаем корневой элемент текущих комментариев
            root = ET.fromstring(self.__xml_comments)
            # Получаем необходимый нам комментарий по его id
            for comment in root.iter('comment'):
                if comment.get('id') == str(id_comment):
                    # Меняем рейтинг
                    comment.set('rating', str(int(comment.get('rating')) -1))
                    # Сохраняем все
                    self.__xml_comments = ET.tostring(root)
                    return True
            return False
        else:
            return False

    def get_count(self) -> int:
        """ Узнать сколько всего оставлено комментариев """
        if self.__xml_comments:
            # Получаем корневой элемент текущих комментариев
            root = ET.fromstring(self.__xml_comments)
            comments = root.findall(".//comment")
            return len(comments)
        else:
            return 0

    # VIEWS TREE

    def print_comment(self, id_comment: int) -> None:
        """Отображает информацию о комментарии"""
        if self.__xml_comments:
            # Получаем корневой элемент текущих комментариев
            root = ET.fromstring(self.__xml_comments)
            # Получаем необходимый нам комментарий по его id
            for comment in root.iter('comment'):
                if comment.get('id') == str(id_comment):
                    print("id:" + comment.get("id"))
                    print("user_id:" + comment.get("user_id"))
                    print("user_name:" + comment.get("user_name"))
                    print("answered_id:" + comment.get("answered_id"))
                    print("answered_name:" + comment.get("answered_name"))
                    print("date:" + comment.get("date"))
                    print("rating:" + comment.get("rating"))
                    print("is_edit:" + comment.get("is_edit"))
                    print("is_claim:" + comment.get("is_claim"))
                    print("is_moderator:" + comment.get("is_moderator"))
                    print("text:" + comment.get("text"))
                    return True
            return False
        else:
            return False

    def debug_comment(self, id_comment: int) -> tuple:
        """Возвращает все параметры комментария в виде кортежа. Необходимо для тестирования."""
        if self.__xml_comments:
            # Получаем корневой элемент текущих комментариев
            root = ET.fromstring(self.__xml_comments)
            # Получаем необходимый нам комментарий по его id
            for comment in root.iter('comment'):
                if comment.get('id') == str(id_comment):
                    # Cоставляем список
                    resultParam = []
                    resultParam.append(comment.get("id"))
                    resultParam.append(comment.get("user_id"))
                    resultParam.append(comment.get("user_name"))
                    resultParam.append(comment.get("answered_id"))
                    resultParam.append(comment.get("answered_name"))
                    resultParam.append(comment.get("date"))
                    resultParam.append(comment.get("rating"))
                    resultParam.append(comment.get("is_edit"))
                    resultParam.append(comment.get("is_claim"))
                    resultParam.append(comment.get("is_moderator"))
                    resultParam.append(comment.get("text"))
                    # Возвращаем кортеж
                    return tuple(resultParam)
            return ()
        else:
            return ()

    # TODO: Реализовать. Может, когда-нибудь пригодится для отладки
    def print(self) -> None:
        """Отображает красиво все комментарии"""
        pass

    def print_xml(self) -> None:
        """Отображает отформатировнную xml строку текущих комментариев."""
        if self.__xml_comments is not None:
            print(self.__format_xml(self.__xml_comments))

    # WORK WITH CONVERTING

    # ------------------------------------------------
    # Variant 1 --------------------------------------
    # ------------------------------------------------
    def to_html(self, is_dynamic=False) -> str:
        """Конвертурует в html фронтенд для комментариев."""
        if self.__xml_comments:
            # Получаем корневой элемент текущих комментариев
            root = ET.fromstring(self.__xml_comments)
            root_ul = ET.Element('ul')
            root_ul.set('class', 'media-list')
            # Проходим по всем комментариям и создаем <li> для каждого
            comments = root.findall('./comment')
            for comment in comments:
                new_li = ET.Element('li')
                new_li.set('class', 'media')
                root_ul.append(new_li)
                self.__append_html_comment(comment, new_li, is_dynamic)
            # Преобразуем xml в отформатировнную строчку
            result_str = self.__format_xml(ET.tostring(root_ul))
            # Обрабатываем пути к аватаркам
            result_str = result_str.replace('"#path_to_avatar#"', "\"/static/wiki/images/avatars/avatar.jpg\"")
            # Возвращая строчку, убираем в ней первую строку(xml decloration)
            return result_str[result_str.find('\n'):]
        else:
            return None

    # ----------------
    # Private methods:
    # ----------------

    # ------------------------------------------------
    # Variant 1 --------------------------------------
    # ------------------------------------------------
    def __append_html_comment(self, comment, new_div, is_dynamic):
        """ Генерация html для варианта 1"""
        media_left = ET.Element('div')
        media_left.set('class', 'media-left')
        media_left_href = ET.Element('a')
        media_left_href.set('href', '#')
        new_img = ET.Element('img')
        new_img.set('class', 'media-object img-rounded')
        new_img.set('src', '#path_to_avatar#')
        new_img.set('alt', '...')
        media_left_href.append(new_img)
        media_left.append(media_left_href)
        new_div.append(media_left)
        media_body = ET.Element('div')
        media_body.set('class', 'media-body')
        media_heading = ET.Element('div')
        media_heading.set('class', 'media-heading')
        author = ET.Element('div')
        author.set('class', 'author') #/user/2/
        author_href = ET.Element('a')
        author_href.set('href', '/user/'+str(comment.get('user_id')))
        author_href.text = comment.get('user_name')
        author.append(author_href)
        meta_data = ET.Element('div')
        meta_data.set('class', 'metadata')
        span_date = ET.Element('span')
        span_date.set('class', 'date')
        span_date.text = comment.get('date')
        meta_data.append(span_date)
        media_heading.append(author)
        media_heading.append(meta_data)
        media_body.append(media_heading)
        media_text = ET.Element('div')
        media_text.set('class', 'media-text text-justify')
        media_text.text = comment.get('text')
        media_body.append(media_text)
        footer_comment = ET.Element('div')
        footer_comment.set('class', 'footer-comment')
        span_plus = ET.Element('span')
        span_plus.set('class', 'vote plus comment-rating-up')
        span_plus.set('id_comment', comment.get('id'))
        span_plus.set('title', 'Нравится')
        icon_plus = ET.Element('i')
        icon_plus.text = ' '
        icon_plus.set('class', 'fa fa-thumbs-up')
        span_plus.append(icon_plus)
        span_rating = ET.Element('span')
        span_rating.set('class', 'rating')
        span_rating.text = comment.get('rating')
        span_minus = ET.Element('span')
        span_minus.set('class', 'vote minus comment-rating-down')
        span_minus.set('id_comment', comment.get('id'))
        span_minus.set('title', 'Не нравится')
        icon_minus = ET.Element('i')
        icon_minus.set('class', 'fa fa-thumbs-down')
        icon_minus.text = ' '
        span_minus.append(icon_minus)
        span_devide = ET.Element('span')
        span_devide.set('class', 'devide')
        span_devide.text = '|'
        span_comment_reply = ET.Element('span')
        span_comment_reply.set('class', 'comment-reply')
        href_reply = ET.Element('a')
        if not is_dynamic:
            href_reply.set('class', 'reply main-comment-reply')
            href_reply.set('data-toggle', 'modal')
            href_reply.set('data-target', '#modal_main_comment')
        else:
            href_reply.set('class', 'reply dynamic-comment-reply')
            href_reply.set('data-toggle', 'modal')
            href_reply.set('data-target', '#modal_dynamic_comment_reply')
        href_reply.set('id_comment', comment.get('id'))
        href_reply.text = 'ответить'
        span_comment_reply.append(href_reply)
        footer_comment.append(span_plus)
        footer_comment.append(span_rating)
        footer_comment.append(span_minus)
        footer_comment.append(span_devide)
        footer_comment.append(span_comment_reply)
        media_body.append(footer_comment)
        new_div.append(media_body)
        comments = comment.findall('./comment')
        for child_comment in comments:
            new_child_div = ET.Element('div')
            new_child_div.set('class', 'media')
            media_body.append(new_child_div)
            self.__append_html_comment(child_comment, new_child_div, is_dynamic)

    def __format_xml(self, xml_str):
        """Выравнивание xml строки"""
        return parseString(xml_str).toprettyxml()

