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
from WikiCode.apps.wiki.src.future.wiki_search.config import params as CONFIG


# TODO: Добавить тестирующий класс
class WikiSearch():
    """
       :VERSION: 0.1
       Класс отвечающий за весь поиск в платформе.
       Должен уметь искать по:
       - Тексту конспектов
       - Авторам конспектов
       - Описанию конспектов
       - Заголовкам конспектов
       - По комментариям в конспектах
       - По папкам
       - По тегам
       - По личным уведомлениям, коллегам(в будущем)
       - Абсолютный поиск(ищет конспекты по всему)

       Поиск должен быть настраиваемым и запросы должны быть настраиваемыми.
       """
    def __init__(self):
        pass

    # ---------------
    # Public methods:
    # ---------------


    # ----------------
    # Private methods:
    # ----------------

