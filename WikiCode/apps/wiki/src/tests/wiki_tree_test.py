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


# ---------------------- #
# ТЕСТЫ ДЛЯ WIKITREE #
# ---------------------- #

from WikiCode.apps.wiki.src.wiki_tree import WikiTree


def test_wiki_tree_1():
    wt = WikiTree(0)
    assert wt.get_tree() == 'user_id=0\nPersonal/:0\nImports/:0\n'


def test_wiki_tree_2():
    wt = WikiTree(-1)
    assert wt.get_tree() is None


def test_wiki_tree_3():
    wt = WikiTree("fhf")
    assert wt.get_tree() is None


def test_wiki_tree_4():
    wt = WikiTree(0)
    wt.add_folder("Personal/","NewFolder")
    assert wt.get_tree() == 'user_id=0\nPersonal/:0\nImports/:0\nPersonal/NewFolder/:0\n'
