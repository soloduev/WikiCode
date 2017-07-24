#   # -*- coding: utf-8 -*-
#
#   Copyright (C) 2017 Igor Soloduev <diahorver@gmail.com>
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

# Здесь хранятся константы и настройки сайта, которые необходимо настроить при запуске или сопровождении сайта
# Также, здесь хранится настройка всех модулей

# ---------------------------------------------------------------------------#
# НАСТРОЙКА БЕКАПОВ----------------------------------------------------------#
# ---------------------------------------------------------------------------#

# В данный момент все захардкожено под gmail почту.
# Для другой почты пока не работает.

# Почта и пароль, с которой будет происходить отправка бекапов:
EMAIL_BACKUP_SENDER_NAME = "wcodetest@gmail.com"
EMAIL_BACKUP_SENDER_PASSWORD = "wcodetest7251955"

# Почта на которую будут отправляться бекапы:
EMAIL_BACKUP_RECEIVER_NAME = "diahorver@gmail.com"

# Тема и текст письма при отправки очередного бекапа
EMAIL_BACKUP_SUBJECT = "Daily backup"
EMAIL_BACKUP_TEXT = "Backup file:\n\n"

# Формат файла бекапа(xml, json)
BACKUP_FILE_FORMAT = "xml"

# Имя файла бекапа(Дата будет подставлена автоматически)
BACKUP_FILE_NAME = "Backup_DB_WikiCode"

# Ширина отступа в тексте файла бекапа(для читаймости)
BACKUP_FILE_INDENT = 2


# ---------------------------------------------------------------------------#
# РЕЖИМ РЕМОНТА--------------------------------------------------------------#
# ---------------------------------------------------------------------------#

# Вход только для разработчиков и тестировщиков
# Если вы хотите, чтобы на сайт могли зайти только разработчики или тестироващики, поставьте True
# В таком случае, на сайт смогут зайти лишь только разработчики.
# Для того, чтобы стать разработчиком, необходимо зарегестрироваться на сайте под именем dev_<ваш nickname>
# Затем, администратор сайта в базе данных должен вас добавить как разработчика с тем же именем
# Все, теперь вы зарегестрированы как разработчик и сможете зайти на сайт, кликнув на слово "разработчикам"
DEVELOP_MODE = False

# ---------------------------------------------------------------------------#
# ТЕСТИРОВАНИЕ ПЛАТФОРМЫ-----------------------------------------------------#
# ---------------------------------------------------------------------------#

# Активация тестов, при запуске сервера.
RUN_TESTS = False

# Если тесты не успешны, то сервер не запускается.

# ---------------------------------------------------------------------------#
# МОДУЛИ ПЛАТФОРМЫ ----------------------------------------------------------#
# ---------------------------------------------------------------------------#

# ---------------------------------------------------------------------------#
# 1.Динамические параграфы --------------------------------------------------#
# ---------------------------------------------------------------------------#

MODULE_DYNAMIC_PARAGRAPHS = True  # Активация модуля

# ---------------------------------------------------------------------------#
# 2.Общие комментарии -------------------------------------------------------#
# ---------------------------------------------------------------------------#

MODULE_MAIN_COMMENTS = True  # Активация модуля

# ---------------------------------------------------------------------------#
# 3.Версии конспекта --------------------------------------------------------#
# ---------------------------------------------------------------------------#

MODULE_VERSIONS = True  # Активация модуля

# ---------------------------------------------------------------------------#
# ПРОЧИЕ НАСТРОЙКИ ПЛАТФОРМЫ ------------------------------------------------#
# ---------------------------------------------------------------------------#

# ---------------------------------------------------------------------------#
# index.html ----------------------------------------------------------------#
# ---------------------------------------------------------------------------#

COUNT_LAST_PUBL_SHOW = 100  # Какое количество последних публикаций отображать на главной странице

