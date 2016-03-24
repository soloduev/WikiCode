# -*- coding: utf-8 -*-

# Менеджер по управлению деревьями в WikiCode. version 0.1:


class WikiTree(object):
    def __init__(self, user_id):
        self.tree = "user_id=" + str(user_id) + "\n"
        self.tree += "Personal/:" + str(user_id) + "\n"
        self.tree += "Imports/:" + str(user_id) + "\n"
        self.user_id = str(user_id)

    def printTree(self):
        print(self.tree)

    def addFolder(self, path, name_folder):
        """
        Добавление папки в дерево.
        Обязательно необходимо указывать правильный путь к папке. Папка всегда заканчивается на /.
        Если вы хотите создать глобальную папку, в аргумент path передаете строку 'global'.
        Добавление в папку Imports этим методом запрещено! Это нарушает нотацию файла wikicode дерева.
        """
        if path == "global":
            if not self.isLine(name_folder + "/"):
                self.tree += name_folder + "/:" + self.user_id + "\n"
        if self.isLine(path) and not self.isLine(path + name_folder + "/"):
            self.tree += path + name_folder + "/:" + self.user_id + "\n"

    def addPublication(self, path, name_publ, id_publ):
        """
        Первый параметр -  папка, в которой размещаем публикацию.
        Строка пути к папке обязательно должна заканчиваться на /.
        Второй параметр - это ваше название публикации. Оно не должно повторятся в текущей папке.
        Третий параметр - это id данной публикации.
        """
        if self.isLine(path) and not self.isLine(path + str(name_publ) + ".publ"):
            self.tree += path + name_publ + ".publ:" + str(id_publ) + "\n"
        pass

    def isLine(self, findLine):
        isFind = False
        numLine = 0
        treeLines = self.tree.split("\n")
        for i in range(1, len(treeLines)):
            if treeLines[i].split(":")[0] == findLine:
                isFind = True
                numLine += 1
        if numLine == 1 and isFind == True:
            return True
        else:
            return False

    def printFirstPath(self):
        """Напечатать в виде строки самый верхний уровень дерева"""
        total = ""
        paths = self.tree.split("\n")
        for i in range(1, len(paths)):
            path = paths[i].split(":")[0]
            if path.count("/") == 1 and path.count(".publ") == 0:
                total += path + "\n"
        print(total)

    def printPathContent(self, path_folder):
        """Напечатать в виде строки все содержание конкретной папки"""
        # Количество уровней в той папке, которую ищем
        num_levels = path_folder.count("/")
        total = ""
        paths = self.tree.split("\n")
        for i in range(1, len(paths)):
            path = paths[i].split(":")[0]
            if path.__contains__(path_folder) and path != path_folder:
                if path.count("/") == num_levels:
                    total += path.split("/")[num_levels] + "\n"
                elif path.count("/") == num_levels + 1 and path.count(".publ") == 0:
                    total += path.split("/")[num_levels] + "/\n"
        print(total)

    def renamePublication(self, path_publ, new_name):
        """Изменяет имя публикации по указанному пути"""
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

    def deletePublication(self, path_publ):
        """Удаляет публикацию по указанному пути"""
        paths = self.tree.split("\n")
        for i in range(1, len(paths)):
            path = paths[i].split(":")[0]
            if path == path_publ:
                new_tree = ""
                for n in range(0, len(paths)):
                    if n != i:
                        new_tree += paths[n] + "\n"
                self.tree = new_tree

    def deleteFolder(self, path_folder):
        """Удаляет папку и все ее внутреннее содержимое по указанному пути"""
        paths = self.tree.split("\n")
        for i in range(1, len(paths)):
            path = paths[i].split(":")[0]
            if path == path_folder:
                new_tree = ""
                for n in range(0, len(paths)):
                    if n != i and paths[n].find(path_folder) != 0:
                        new_tree += paths[n] + "\n"
                self.tree = new_tree

    def getNumsPublications(self):
        """Возвращает количество публикаций в дереве"""
        total = 0
        paths = self.tree.split("\n")
        for i in range(1, len(paths)):
            path = paths[i].split(":")[0]
            if path.__contains__(".publ"):
                total += 1
        return total;

    def getAllPublicationsPaths(self):
        """Возвращает пути ко всем публикациям в дереве, в виде списка"""
        total = []
        paths = self.tree.split("\n")
        for i in range(1, len(paths)):
            path = paths[i].split(":")[0]
            if path.__contains__(".publ"):
                total.append(path)
        return total

    def getParamPublication(self, path_publ, num_param):
        """Возвращает значение параметра публикации"""
        paths = self.tree.split("\n")
        for i in range(1, len(paths)):
            path = paths[i].split(":")[0]
            if path == path_publ:
                return paths[i].split(":")[num_param]

    def printAllPublicationsPaths(self):
        """Печатает пути ко всем публикациям в дереве"""
        total = []
        paths = self.tree.split("\n")
        for i in range(1, len(paths)):
            path = paths[i].split(":")[0]
            if path.__contains__(".publ"):
                print(path)

    def renameFolder(self, path_folder, new_name):
        """
        Переименовывает папку.
        Первый аргумент - путь к папке которую переименовываем.
        Второй аргумент - новое имя этой папки.
        """
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
                if not self.isLine(new_path):
                    self.tree = self.tree.replace(paths[index], new_path + ":" + paths[index].split(":")[1])
                    # Также меняем название папки везде где это необходимо
                    treeLines = self.tree.split("\n")
                    for i in range(1, len(treeLines)):
                        if treeLines[i].find(path_folder) == 0:
                            new_line = treeLines[i].replace(path_folder, new_path)
                            self.tree = self.tree.replace(paths[i], new_line)


# Testing class
wt = WikiTree(124)
wt.addFolder("global", "My")
wt.addFolder("global", "MyLessons")
wt.addFolder("MyLessons/", "Java");
wt.addFolder("My/", "Configures")
wt.addFolder("My/", "Configures")
wt.addFolder("MyLessons/Java/", "Configures")
wt.addPublication("My/", "about", 342)
wt.addPublication("My/", "l1", 355)
wt.addPublication("My/", "l2", 357)
wt.addFolder("My/", "NewFolder")
wt.addPublication("My/NewFolder/", "new", 665)
wt.addFolder("MyLessons/Java/", "Spring")
wt.addPublication("MyLessons/Java/", "hello_world!", 773)
wt.addPublication("MyLessons/Java/", "Основы языка", 777)
wt.addPublication("MyLessons/Java/", "Контейнеры", 780)
wt.printTree()
print("test paths:")
wt.printFirstPath()
print("getPathContent:")
wt.printPathContent("My/NewFolder/")
wt.renameFolder("My/NewFolder/", "hahah");
wt.renameFolder("MyLessons/Java/", "C++");
wt.renameFolder("My/", "You");
wt.renamePublication("MyLessons/C++/Контейнеры.publ", "Массивы")
wt.renamePublication("You/about.publ", "Об авторе")
wt.deletePublication("You/hahah/new.publ")
wt.printTree()
wt.addFolder("You/hahah/", "secretFolder")
print("---------------")
wt.printPathContent("You/hahah/")
print("----------")
print(wt.getNumsPublications())
wt.printAllPublicationsPaths()
print(wt.getParamPublication("MyLessons/C++/Массивы.publ", 1))
print("-------------")
wt.deleteFolder("MyLessons/C++/")
wt.printTree()
