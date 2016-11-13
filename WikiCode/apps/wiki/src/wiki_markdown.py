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


# WikiMarkdown version 0.4
# Класс для разбивки Markdown текста на логические абзацы
# Возможности:
# Может разбивать
# -Заголовки
# -Обычный текст
# -Участки кода обозначенные как ```
# -Участи кода обозначенные отступами в 4 пробела
# -Списки


class WikiMarkdown(object):
    def __init__(self):
        pass

    def split(self, markdown_text):
        """Главный метод. Разбивает markdown текст на логические абзацы"""

        # Сначала разбиваем текст построчно
        lines = self.__split_lines(markdown_text)

        # Далее проходим по строкам и создаем логические абзацы
        # Итоговый список логических абзацев
        paragraphs = []
        logic_paragraph = ""
        index = 0
        while index < len(lines):
            # Если начался блок кода
            # Формируем логический абзац до тех пор, пока блок кода не закроется
            if self.__is_start_end_code(lines[index]):
                if logic_paragraph!="":
                    paragraphs.append(logic_paragraph)
                    logic_paragraph = ""
                logic_paragraph+=lines[index]+"\n"
                index+=1
                is_end = False
                while index < len(lines):
                    if self.__is_start_end_code(lines[index]):
                        if logic_paragraph.count("\n") != 1:
                            logic_paragraph += lines[index] + "\n"
                            paragraphs.append(logic_paragraph)
                            logic_paragraph = ""
                            is_end = True
                            break
                        else:
                            logic_paragraph = ""
                            break
                    else:
                        logic_paragraph += lines[index] + "\n"
                    index+=1
                if not is_end:
                    logic_paragraph += "```\n"
                    paragraphs.append(logic_paragraph)
                    logic_paragraph = ""
                index += 1
            elif self.__is_code_tab(lines[index]):
                if logic_paragraph != "":
                    paragraphs.append(logic_paragraph)
                    logic_paragraph = ""
                logic_paragraph += lines[index] + "\n"
                index += 1
                is_end = False
                while index < len(lines):
                    if not self.__is_code_tab(lines[index]):
                        paragraphs.append(logic_paragraph)
                        logic_paragraph = ""
                        is_end = True
                        break
                    else:
                        logic_paragraph += lines[index] + "\n"
                    index += 1
                if not is_end:
                    paragraphs.append(logic_paragraph)
                    logic_paragraph = ""
            elif self.__is_line_split(lines[index]):
                if len(paragraphs) >= 1:
                    paragraphs[len(paragraphs)-1] += lines[index] + "\n"
                    logic_paragraph = ""
                    index+=1
                else:
                    paragraphs.append(lines[index] + "\n")
                    logic_paragraph = ""
                    index += 1
            elif self.__is_title_line(lines[index]):
                if len(paragraphs) >= 1:
                    paragraphs[len(paragraphs) - 1] += lines[index] + "\n"
                    logic_paragraph = ""
                    index += 1
                else:
                    paragraphs.append(lines[index] + "\n")
                    logic_paragraph = ""
                    index += 1
            elif self.__is_start_end_lists(lines[index]):
                if logic_paragraph != "":
                    paragraphs.append(logic_paragraph)
                    logic_paragraph = ""
                logic_paragraph += lines[index] + "\n"
                index += 1
                is_end = False
                while index < len(lines):
                    if not self.__is_start_end_lists(lines[index]):
                        paragraphs.append(logic_paragraph)
                        logic_paragraph = ""
                        is_end = True
                        break
                    else:
                        logic_paragraph += lines[index] + "\n"
                    index += 1
                if not is_end:
                    paragraphs.append(logic_paragraph)
                    logic_paragraph = ""
            elif self.__is_void(lines[index]):
                logic_paragraph = ""
                index += 1
            else:
                if logic_paragraph == "":
                    logic_paragraph += lines[index] + "\n"
                    paragraphs.append(logic_paragraph)
                    logic_paragraph = ""
                    index+=1


        return paragraphs

    def generate_contents(self, paragraphs: []):
        """ Генерирует оглавление для конспекта. Необходимо передать отдельные параграфы конпекта в иде списка. """
        result_contents = ""
        cur_lvl = 1

        for paragraph in paragraphs:

            if len(paragraph["text"]) > 4:
                if paragraph["text"][0:2] == '# ' and paragraph["text"][-3:] == " #\n":
                    result_contents += str(cur_lvl) + ". [" + paragraph["text"][2:-2] + "](/page/3/#1)\n"
                    cur_lvl+=1
            if len(paragraph["text"]) > 6:
                if paragraph["text"][0:3] == '## ' and paragraph["text"][-4:] == " ##\n":
                    result_contents += "    - [" + paragraph["text"][3:-3] + "](/page/3/#2)\n"
            if len(paragraph["text"]) > 9:
                if paragraph["text"][0:4] == '### ' and paragraph["text"][-5:] == " ###\n":
                    result_contents += "     - [" + paragraph["text"][4:-4] + "](/page/3/#3)\n"

        if result_contents == "":
            return "### Заголовки в конспекте не были определены. ###\n### Оглавление не сгенерировано ###"

        return result_contents


    def print_paragraphs(self, paragraphs: []):
        for line in paragraphs:
            print(line, end="")
            print("____________")


    def __split_lines(self, text: str) -> []:
        """Разбивает текст на строчки. Возвращает список строк"""
        lines = text.split("\n")
        return lines

    def __is_title(self, line: str) -> bool:
        """Проверяет, является ли строка заголовком"""
        if line.find("#") == 0:
            return True
        else:
            return False

    def __is_start_end_code(self, line: str) -> bool:
        """Проверяет, начало это блока кода или конец"""
        if line.find("```") == 0:
            return True
        else:
            return False

    def __is_code_tab(self, line: str) -> bool:
        """Проверяет, блок ли это кода"""
        if line.find("    ") == 0:
            return True
        else:
            return False

    def __is_quote_block(self, line: str) -> bool:
        """Проверяет, блок ли это цитаты"""
        if line.find(">") == 0:
             return True
        elif line.find(" >") == 0:
            return True
        elif line.find("  >") == 0:
            return True
        elif line.find("   >") == 0:
            return True
        else:
            return False

    def __is_void(self, line: str) -> bool:
        is_empty = True
        if line == "":
            return True
        for char in line:
            if char != " " and char != "\n" and char != "\r":
                is_empty = False
        return is_empty

    def __is_line_split(self, line: str) -> bool:
        """Проверяем, разделяющая ли это линия?"""
        if line.find("* * *") == 0:
            return True
        else:
            return False

    def __is_title_line(self, line: str) -> bool:
        """Проверяем, это не линия заголовка?"""
        is_line = True
        if line == "":
            return False
        else:
            if line[0] == "=" or line[0] == "-":
                for char in line:
                    if char != "=" and char != "-" and char != "\r":
                        is_line = False
                return is_line
            else:
                return False

    def __is_start_end_lists(self, line: str) -> bool:
        """Проверяет, начало это блока списка или конец"""
        length_line = len(line)
        if line.find(".") == 1:
            if str(type(int(line[0]))) == "<class 'int'>":
                return True
        if line.find(".") == 2:
            if str(type(int(line[0]))) == "<class 'int'>" and str(type(int(line[1]))) == "<class 'int'>":
                return True
        if line.find(".") == 3:
            if str(type(int(line[0]))) == "<class 'int'>" and str(type(int(line[1]))) == "<class 'int'>" and str(type(int(line[2]))) == "<class 'int'>":
                return True

        if length_line >= 2:
            if line[0] == "*" and line[1] == " ":
                return True
            elif line[0] == "-" and line[1] == " ":
                return True
            elif line[0] == " " and line[1] == "*":
                return True
            elif line[0] == " " and line[1] == "-":
                return True
            else:
                return False

