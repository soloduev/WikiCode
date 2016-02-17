
# Парсит Markdown текст и возвращает массив абзацев
def mdSplit(markdown_text):
    arrParagraph = []
    paragraph = ""
    codeParagraph = ""
    sizeLines = howLines(markdown_text)
    startCodeBlock = False
    # Проход по линиям текста
    for i in range(0,sizeLines):
        line = cutLine(markdown_text)
        length = len(line)
        markdown_text = markdown_text[length:]
        #Если активирован блок кода
        if startCodeBlock:
            paragraph += line
            codeParagraph += line
            if isCodeBlock(line) == True:
                arrParagraph.append(codeParagraph)
                paragraph = ""
                codeParagraph = ""
                startCodeBlock = False
        # Правило 1
        elif isHeader(line):
            if paragraph != "":
                arrParagraph.append(paragraph)
            paragraph = ""
            arrParagraph.append(line)
        # Правило 2
        elif isCodeBlock(line):
            arrParagraph.append(paragraph)
            paragraph = ""
            paragraph += line
            codeParagraph = ""
            codeParagraph += line
            startCodeBlock = True
        # Правило 3
        elif isLine(line):
            paragraph += line
            arrParagraph.append(paragraph)
            paragraph = ""
        else:
            paragraph += line

    if paragraph != "":
        arrParagraph.append(paragraph)

    return arrParagraph


# Возвращает первую строку из текста
def cutLine(text):
    line = ""
    for ch in text:
        if ch == '\n':
            line += ch
            break
        else:
            line += ch
    return line


# Узнает, сколько строк в тексте
def howLines(text):
    result = 0
    for ch in text:
        if ch == '\n':
            result += 1
    return result


# Правило 1
# Возвращает true если это заголовок и уровень заголовка
def isHeader(line):
    headerLevel = 0
    for ch in line:
        if ch == '#':
            headerLevel += 1
        else:
            break;
    if headerLevel == 0:
        return False
    elif headerLevel <= 5:
        return True
    else:
        return False


# Правило 2
# Возвращает true если эта строка является началом или концом блока кода
def isCodeBlock(line):
    if line == "```\n":
        return True
    else:
        return False


# Правило 3
# Если это строка линия, то вовзращаем true
def isLine(line):
    if line == "* * *\n" or line == "***\n":
        return True
    else:
        return False
