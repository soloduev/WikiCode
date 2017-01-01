#   # -*- coding: utf-8 -*-
#
#   Copyright (C) 2016-2017 Igor Soloduev <diahorver@gmail.com>
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


class WikiNotify:

    @staticmethod
    def generate_add_colleague(author_nickname, author_email, author_id, author_text):
        """ Генерирует html уведомления для добавления пользователя в коллеги """
        result_html = "<div class=\"text-left\">"
        result_html += "<span><b>Пользователь:</b> <a href='/user/" + str(author_id) + "'/>"
        result_html += str(author_nickname) + "</a> | " + str(author_email) + "</span>"
        result_html += "<br>"
        result_html += "<span>Просит Вас добавить его в коллеги.</span>"
        result_html += "<br><br>"
        result_html += "<span><b>Сообщение:</b></span>"
        result_html += "<br>"
        result_html += "<span>" + author_text + "</span>"
        result_html += "<br>"
        result_html += "<hr>"
        result_html += "</div>"
        result_html += "<div class=\"text-right\"><button type=\"submit\" class=\"btn\" id=\"wiki-style-btn\">Добавить в коллеги</button></div>"

        return result_html