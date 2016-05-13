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


# Здесь хранятся константы и настройки сайта, которые необходимо настроить при запуске сайта

# Вход только для разработчиков и тестировщиков
# Если вы хотите, чтобы на сайт могли зайти только разработчики или тестироващики, поставьте True
# В таком случае, на сайт смогут зайти лишь только разработчики.
# Для того, чтобы стать разработчиком, необходимо зарегестрироваться на сайте под именем dev_<ваш nickname>
# Затем, администратор сайта в базе данных должен вас добавитьк как разработчика с тем же именем
# Все, теперь вы зарегестрированы как разработчик и сможете зайти на сайт, кликнув на слово "разработчикам"
DEVELOP_MODE = False

