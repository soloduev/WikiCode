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


# ФАЙЛ КОНФИГУРАЦИИ РАБОТЫ WIKITREE

params = {

    # ПАРАМЕТРЫ ПАПОК

    # Запрещенные символы для наименования папки
    # Deprecated Symbols For Folder
    "DSFF": {"\"", "\'"},

    # Возможные варианты доступа папки
    # Folder Access Values
    "FAV": {"public", "private"},

    # Возможные варианты типов папки
    # Folder Types Values
    "FTV": {"personal", "saved"},

    # Возможные варианты стилей папки
    # Folder Styles Values
    "FSV": {"default", "red", "blue", "yellow", "green", "black"},

    # Возможные варианты вида папки
    # Folder View Values
    "FVV": {"closed","open"},

    # ПАРАМЕТРЫ КОНСПЕКТОВ

    # Запрещенные символы для наименования конспекта
    # Deprecated Symbols For Publication
    "DSFP": {"\"", "\'"},

}

# ШАБЛОНЫ ДЛЯ ГЕНЕРАЦИИ ФРОНТЕДА И ФУНКЦИИ

def generate_html_dynamic(template_values: tuple) -> str:
    """Сюда помещается шаблон кода, который необходим фронтенду.
    Данный метод его генерирует, подставляя в него по порядку строковые переменные из поданного в него кортежа."""
    # ---------------------------------
    # ШАБЛОН ДИНАМИЧЕСКОГО ФАЙЛОВОГО ДЕРЕВА
    # ---------------------------------
    html_template = """
    <comment id="%s">
        <a id="%s" name="%s"></a>
    </comment>
    """ % tuple(template_values)
    # ---------------------------------
    # ---------------------------------
    return html_template


def generate_html_preview(template_values: tuple) -> str:
    """Сюда помещается шаблон кода, который необходим фронтенду.
    Данный метод его генерирует, подставляя в него по порядку строковые переменные из поданного в него кортежа."""
    # ---------------------------------
    # ШАБЛОН ПРЕВЬЮ ДЕРЕВА
    # ---------------------------------
    html_template = """
    <comment id="%s">
        <a id="%s" name="%s"></a>
    </comment>
    """ % tuple(template_values)
    # ---------------------------------
    # ---------------------------------
    return html_template
