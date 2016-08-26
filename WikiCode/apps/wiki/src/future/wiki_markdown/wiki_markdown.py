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
from WikiCode.apps.wiki.src.future.wiki_markdown.config import params as CONFIG


class WikiMarkdown():
    """
       :VERSION: 0.1
       Класс для парсинга markdown текста.
       Основная задача класса - делить markdown текст на абзацы и возвращать их в виде списка.
       Также, он работает с расширенным WikiCode синтаксисом для маркадаун текста.
       Такие вещи как, формулы, таблицы, деревтя, UML, код, тесты, фреймы для вопросов, особые ссылки и прочее.
       Все дополнения должны настраиваться в конфигурационном файле.
       """
    def __init__(self, md_text: str):
        self.__md_text = md_text

    # ---------------
    # Public methods:
    # ---------------

    def load(self, md_text: str):
        """Загрузить маркдаун текст"""
        pass

    def split(self) -> list:
        """Возвращает все абзацы из маркдаун текста."""
        pass

    def setup(self, options: tuple):
        """Задать настройки парсеру"""
        pass

    def check(self, md_text: str):
        """Функция проверяет на наличие конфликтов в тексте"""
        pass

    # ----------------
    # Private methods:
    # ----------------

