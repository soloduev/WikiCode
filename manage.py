#!/usr/bin/env python
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


import os
import sys

from WikiCode.apps.wiki.settings import wiki_settings
from WikiCode.apps.wiki.src.wiki_tests import WikiTests

# Если активирован модуль тестирования, запускаем сначала его

STOP_SERVER = False

if wiki_settings.RUN_TESTS:
    wiki_tests = WikiTests()
    ERRORS_NOT_FOUND = wiki_tests.run()

    # Если включен модуль жесткого тестировния, то при обнаружении ошибки, перезапускаем сервер
    if wiki_settings.HARD_TESTS and not ERRORS_NOT_FOUND:
        STOP_SERVER = True


if not STOP_SERVER:
    if __name__ == "__main__":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WikiCode.settings")

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)
