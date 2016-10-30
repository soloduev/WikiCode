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


# В таком виде содержиться граф и его связи

graph = {
    1: [2],
    2: [3, 1],
    3: [11, 4, 2],
    4: [5,6,7, 3],
    5: [9, 4],
    6: [8, 4],
    7: [8, 13, 4],
    8: [10, 6, 7],
    9: [10, 5],
    10: [11, 9, 8],
    11: [12, 3, 10],
    12: [11],
    13: [7],
}

# В таком виде содержится информация о версии
vers = {
    1: {
        "id_user": 453,
        "commit_msg": 'Some message...',
        "comments": [],
        "diff": [],
        "date": 'some date...',
        "type": 'Head(H), Root(R), Leaf(L), Merge(M), Node(N)',
        "seq": 'if this is head',
        "branch": 'branch name',
    },
    2: {
        # ...
    },
    # etc..
}

# Также, хранится индекс Head версии
head_index = 12


