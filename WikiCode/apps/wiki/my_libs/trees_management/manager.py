# -*- coding: utf-8 -*-

# Менеджер по управлению деревьями в WikiCode. version 0.2:


class WikiTree(object):
    def __init__(self, user_id):
        if str(type(user_id)) == "<class 'int'>":
            if not user_id < 0:
                self.tree = "user_id=" + str(user_id) + "\n"
                self.tree += "Personal/:" + str(user_id) + "\n"
                self.tree += "Imports/:" + str(user_id) + "\n"
                self.user_id = str(user_id)
            else:
                self.__print_error("user_id < 0")
        else:
            self.__print_error("user_id not int")

    def generate_html_preview(self):
        """Генерирует html текст превью wiki дерева"""

        # Сначала генерируем супер карту
        paths = self.tree.split("\n")
        elements = []
        max = 0
        for i in range(1, len(paths)):
            elements.append([
                paths[i],
                self.__get_num_level(paths[i]),
                self.__convert_line_to_html(paths[i]),
                paths[i].split(":")[0]
            ])
            if max < elements[len(elements)-1][1]:
                max = elements[len(elements)-1][1]
            if elements[len(elements)-1][0] == '':
                del elements[len(elements)-1]
        index = 0
        while max != 1:
            if index == len(elements):
                max-=1
                index = 0
                continue
            else:
                elem = elements[index]
                if elem[1] == max:
                    insert_html = elem[2]
                    find_name = ""
                    if self.__get_type(elem[0]) == "folder":
                        first = elem[0][:elem[0].rfind("/")]
                        find_name = first[:first.rfind("/")+1]
                    elif self.__get_type(elem[0]) == "publ":
                        find_name = elem[0][:elem[0].rfind('/')+1]
                    for i in range(0,len(elements)):
                        if elements[i][3] == find_name:
                            elements[i][2] = self.__insert_elem_to_folder(elements[i][2], insert_html)
                            break
                index+=1

        #Теперь компонуем обе папки вместе:
        return elements[0][2] + elements[1][2]


    def __get_type(self, line):
        """Возвращает тип строки: folder или publ или user_id"""
        if line.count(".publ") == 1:
            return "publ"
        if line.count("user_id") == 0:
            return "folder"
        else:
            return "user_id"

    def __convert_line_to_html(self, line):
        """Определяет тип строки и возвращает html блок этой структуры"""
        if line.count(":") != 0:
            split = line.split(":")
            id = split[1]
            path = split[0]
            if path.endswith("/"):
                # Значит это папка
                part1 = '<li><a href="#">'
                path_split = path.split("/")
                part2 = path_split[len(path_split)-2]
                part3 = '</a>\n<ul>\n</ul>\n</li>\n'
                return part1 + part2 + part3
            elif path.endswith(".publ"):
                # Значит это публикация
                part1 = '<li>'
                path_split = path.split("/")
                part2 = path_split[len(path_split)-1]
                part2 = part2[:len(part2)-5]
                part3 = '<a href="#" class="btn btn-xs btn-link"><span class="glyphicon glyphicon-share-alt"></span></a></li>\n'
                return part1 + part2 + part3
        return ""

    def __get_num_level(self, path):
        """Возвращает на каком уровне находится файл"""
        num_slash = path.count("/")
        if path.count(".publ") == 1:
            # Если это публикация
            return num_slash + 1
        else:
            # Если это папка
            return num_slash



    def __insert_elem_to_folder(self, html_folder1, html_folder2):
        """Вставляет папку в конец папки, возвращает получившийся тег"""
        part1 = html_folder1[:html_folder1.rfind("</ul>")]
        return part1 + html_folder2 + '</ul>\n</li>\n'


    def __print_error(self, error_message):
        print("--------WikiTree---Error--------")
        print("Error message:")
        print(error_message)
        print("--------------------------------")

    def __print_message(self, message):
        print(message)

    def __is_line(self, findLine):
        """Вспомогательный метод. Возвращает True, если указанная строка, есть в дереве"""
        is_find = False
        num_line = 0
        tree_lines = self.tree.split("\n")
        for i in range(1, len(tree_lines)):
            if tree_lines[i].split(":")[0] == findLine:
                is_find = True
                num_line += 1
        if num_line == 1 and is_find == True:
            return True
        else:
            return False

    def __is_forbidden_symbols(self, text):
        if text.__contains__("/") or text.__contains__(":") or text.__contains__("."):
            return True
        else:
            return False

    def print_tree(self):
        """Выводит содержимое дерева в виде строк"""
        try:
            print(self.tree)
        except AttributeError:
            self.__print_error("дерево не создано")

    def add_folder(self, path, name_folder):
        """Добавление папки в дерево.
        Обязательно необходимо указывать правильный путь к папке. Папка всегда заканчивается на /.
        Если вы хотите создать глобальную папку, в аргумент path передаете строку 'global'.
        """
        try:
            if str(type(path)) != "<class 'str'>":
                self.__print_error("аргумент path не является строкой")
            elif str(type(name_folder)) != "<class 'str'>":
                self.__print_error("аргумент name_folder не является строкой")
            elif len(path) <= 1 or not path.endswith("/"):
                self.__print_error("аргумент path передан в неверном формате, пример: 'my_lesson/' ")
            elif self.__is_forbidden_symbols(name_folder):
                self.__print_error("аргумент name_folder содержит запреженные символы)")
            elif path == "global":
                if not self.__is_line(name_folder + "/"):
                    self.tree += name_folder + "/:" + self.user_id + "\n"
            elif self.__is_line(path) and not self.__is_line(path + name_folder + "/"):
                self.tree += path + name_folder + "/:" + self.user_id + "\n"
            else:
                self.__print_error("вы указали не верный путь к папке или папка которую вы хотите создать уже существует")
        except AttributeError:
            self.__print_error("дерево не создано")

    def add_publication(self, path, name_publ, id_publ):
        """Первый параметр -  папка, в которой размещаем публикацию.
        Строка пути к папке обязательно должна заканчиваться на /.
        Второй параметр - это ваше название публикации. Оно не должно повторятся в текущей папке.
        Третий параметр - это id данной публикации.
        """
        try:
            if str(type(path)) != "<class 'str'>":
                self.__print_error("аргумент path не является строкой")
            elif len(path) <= 1 or not path.endswith("/"):
                self.__print_error("аргумент path передан в неверном формате, пример: 'my_lesson/' ")
            elif str(type(name_publ)) != "<class 'str'>":
                self.__print_error("аргумент name_publ не является строкой")
            elif self.__is_forbidden_symbols(name_publ):
                self.__print_error("аргумент name_publ содержит запреженные символы)")
            elif str(type(id_publ)) != "<class 'int'>":
                self.__print_error("аргумент id_publ не является целым числом")
            elif id_publ < 0:
                self.__print_error("аргумент id_publ не может быть < 0")
            elif self.__is_line(path) and not self.__is_line(path + str(name_publ) + ".publ"):
                self.tree += path + name_publ + ".publ:" + str(id_publ) + "\n"
            pass
        except AttributeError:
            self.__print_error("дерево не создано")


    def print_first_path(self):
        """Напечатать в виде строк самый верхний уровень дерева"""
        try:
            total = ""
            paths = self.tree.split("\n")
            for i in range(1, len(paths)):
                path = paths[i].split(":")[0]
                if path.count("/") == 1 and path.count(".publ") == 0:
                    total += path + "\n"
            print(total)
        except AttributeError:
            self.__print_error("дерево не создано")

    def print_path_content(self, path_folder):
        """Напечатать в виде строк все содержание конкретной папки"""
        # Количество уровней в той папке, которую ищем
        try:
            if str(type(path_folder)) != "<class 'str'>":
                self.__print_error("аргумент path_folder не является строкой")
            elif len(path_folder) <= 1 or not path_folder.endswith("/"):
                self.__print_error("аргумент path_folder передан в неверном формате, пример: 'my_lesson/' ")
            else:
                num_levels = path_folder.count("/")
                total = ""
                paths = self.tree.split("\n")
                for i in range(1, len(paths)):
                    path = paths[i].split(":")[0]
                    if path.startswith(path_folder) and path != path_folder:
                        if path.count("/") == num_levels:
                            total += path.split("/")[num_levels] + "\n"
                        elif path.count("/") == num_levels + 1 and path.count(".publ") == 0:
                            total += path.split("/")[num_levels] + "/\n"
                        break
                print(total)
        except AttributeError:
            self.__print_error("дерево не создано")


    def rename_publication(self, path_publ, new_name):
        """Изменяет имя публикации по указанному пути"""
        try:
            if str(type(path_publ)) != "<class 'str'>":
                self.__print_error("аргумент path_publ не является строкой")
            elif len(path_publ) <= 1 or not path_publ.endswith(".publ"):
                self.__print_error("аргумент path_publ передан в неверном формате, пример: 'my_lesson/lesson_1.publ' ")
            elif str(type(new_name)) != "<class 'str'>":
                self.__print_error("аргумент new_name не является строкой")
            elif self.__is_forbidden_symbols(new_name):
                self.__print_error("аргумент new_name содержит запрещенные символы")
            else:
                paths = self.tree.split("\n")
                for i in range(1, len(paths)):
                    path = paths[i].split(":")[0]
                    if path == path_publ:
                        splits = path.split("/")
                        num_levels = path.count("/")
                        splits[num_levels] = new_name + ".publ"
                        new_path = ""
                        for n in range(0, len(splits) - 1):
                            new_path += splits[n] + "/"
                        new_path += new_name + ".publ"
                        new_path += ":" + paths[i].split(":")[1]
                        self.tree = self.tree.replace(paths[i], new_path)
                        break
        except AttributeError:
            self.__print_error("дерево не создано")

    def delete_publication(self, path_publ):
        """Удаляет публикацию по указанному пути"""
        try:
            if str(type(path_publ)) != "<class 'str'>":
                self.__print_error("аргумент path_publ не является строкой")
            elif len(path_publ) <= 1 or not path_publ.endswith(".publ"):
                self.__print_error("аргумент path_publ передан в неверном формате, пример: 'my_lesson/lesson_1.publ' ")
            else:
                paths = self.tree.split("\n")
                for i in range(1, len(paths)):
                    path = paths[i].split(":")[0]
                    if path == path_publ:
                        new_tree = ""
                        for n in range(0, len(paths)):
                            if n != i:
                                new_tree += paths[n] + "\n"
                        self.tree = new_tree
                        break
        except AttributeError:
            self.__print_error("дерево не создано")

    def delete_folder(self, path_folder):
        """Удаляет папку и все ее внутреннее содержимое по указанному пути"""
        try:
            if str(type(path_folder)) != "<class 'str'>":
                self.__print_error("аргумент path_folder не является строкой")
            elif len(path_folder) <= 1 or not path_folder.endswith("/"):
                self.__print_error("аргумент path_folder передан в неверном формате, пример: 'my_lesson/' ")
            else:
                paths = self.tree.split("\n")
                for i in range(1, len(paths)):
                    path = paths[i].split(":")[0]
                    if path == path_folder:
                        new_tree = ""
                        for n in range(0, len(paths)):
                            if n != i and paths[n].find(path_folder) != 0:
                                new_tree += paths[n] + "\n"
                        self.tree = new_tree
                        break
        except AttributeError:
            self.__print_error("дерево не создано")

    def get_nums_publications(self):
        """Возвращает количество публикаций в дереве"""
        try:
            total = 0
            paths = self.tree.split("\n")
            for i in range(1, len(paths)):
                path = paths[i].split(":")[0]
                if path.__contains__(".publ"):
                    total += 1
            return total;
        except AttributeError:
            self.__print_error("дерево не создано")

    def get_all_publications_paths(self):
        """Возвращает пути ко всем публикациям в дереве, в виде списка"""
        try:
            total = []
            paths = self.tree.split("\n")
            for i in range(1, len(paths)):
                path = paths[i].split(":")[0]
                if path.__contains__(".publ"):
                    total.append(path)
            return total
        except AttributeError:
            self.__print_error("дерево не создано")

    def get_param_publication(self, path_publ, num_param):
        """Возвращает значение параметра публикации"""
        try:
            if str(type(path_publ)) != "<class 'str'>":
                self.__print_error("аргумент path_folder не является строкой")
            elif len(path_publ) <= 1 or not path_publ.endswith(".publ"):
                self.__print_error("аргумент path_folder передан в неверном формате, пример: 'my_lesson/lesson_1.publ' ")
            else:
                paths = self.tree.split("\n")
                for i in range(1, len(paths)):
                    path = paths[i].split(":")[0]
                    if path == path_publ:
                        return paths[i].split(":")[num_param]
                        break
        except AttributeError:
            self.__print_error("дерево не создано")
        except IndexError:
            self.__print_error("параметра с индексом "+str(num_param)+" у данной публикации не существует")

    def print_all_publications_paths(self):
        """Печатает пути ко всем публикациям в дереве"""
        try:
            paths = self.tree.split("\n")
            for i in range(1, len(paths)):
                path = paths[i].split(":")[0]
                if path.__contains__(".publ"):
                    print(path)
        except AttributeError:
            self.__print_error("дерево не создано")

    def rename_folder(self, path_folder, new_name):
        """Переименовывает папку.
        Первый аргумент - путь к папке которую переименовываем.
        Второй аргумент - новое имя этой папки.
        """
        try:
            if str(type(path_folder)) != "<class 'str'>":
                self.__print_error("аргумент path_folder не является строкой")
            elif len(path_folder) <= 1 or not path_folder.endswith("/"):
                self.__print_error("аргумент path_publ передан в неверном формате, пример: 'my_lesson/' ")
            elif str(type(new_name)) != "<class 'str'>":
                self.__print_error("аргумент new_name не является строкой")
            elif self.__is_forbidden_symbols(new_name):
                self.__print_error("аргумент new_name содержит запрещенные символы")
            else:
                paths = self.tree.split("\n")
                for i in range(1, len(paths)):
                    path = paths[i].split(":")[0]
                    index = i
                    if path == path_folder:
                        splits = path.split("/")
                        num_levels = path.count("/")
                        splits[num_levels - 1] = new_name
                        new_path = ""
                        for i in range(0, len(splits) - 1):
                            new_path += splits[i] + "/"
                        if not self.__is_line(new_path):
                            self.tree = self.tree.replace(paths[index], new_path + ":" + paths[index].split(":")[1])
                            # Также меняем название папки везде где это необходимо
                            tree_lines = self.tree.split("\n")
                            for i in range(1, len(tree_lines)):
                                if tree_lines[i].find(path_folder) == 0:
                                    new_line = tree_lines[i].replace(path_folder, new_path)
                                    self.tree = self.tree.replace(paths[i], new_line)
                        break
        except AttributeError:
            self.__print_error("дерево не создано")


# Testing class
wt = WikiTree(11)
wt.add_folder("Personal/", "Java")
wt.add_folder("Personal/", "C++")
wt.add_publication("Personal/Java/", "Lesson1", 1)
wt.add_publication("Personal/Java/", "Lesson2", 2)
wt.add_publication("Personal/C++/", "Lesson1", 3)
wt.add_publication("Personal/C++/", "Lesson2", 4)
wt.add_publication("Personal/C++/", "Lesson3", 5)
wt.add_publication("Personal/C++/", "Lesson4", 6)
wt.add_folder("Imports/", "Top")
wt.add_folder("Personal/C++/", "Intermediate")
wt.add_publication("Personal/C++/Intermediate/", "L1", 6)
wt.add_publication("Personal/C++/Intermediate/", "L2", 6)
wt.add_publication("Personal/C++/Intermediate/", "L3", 6)
wt.add_folder("Personal/C++/", "Pro")
wt.add_publication("Personal/C++/Pro/", "Pro1", 6)
wt.add_publication("Personal/C++/Intermediate/", "L4", 6)
wt.add_publication("Personal/C++/", "Lesson5", 6)
wt.add_publication("Personal/C++/", "Lesson6", 6)
wt.add_publication("Personal/C++/Intermediate/", "L6", 6)
wt.add_publication("Personal/C++/Pro/", "Pro2", 6)
wt.add_publication("Personal/C++/Intermediate/", "L7", 6)
wt.add_publication("Personal/C++/Pro/", "Pro3", 6)
wt.add_publication("Personal/C++/Pro/", "Pro4", 6)
wt.add_publication("Personal/C++/Pro/", "Pro5", 6)
wt.add_publication("Personal/C++/Pro/", "Pro6", 6)
wt.print_tree()
print("--------------")
print(wt.generate_html_preview())

