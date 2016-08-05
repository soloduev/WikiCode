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

}
