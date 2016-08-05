from xml.etree import ElementTree as ET


xmlfile = ET.parse("example_wiki_tree.xml")

print(xmlfile)

# Поиск по нодам

print(xmlfile.find('./publication'))

# Получить текст тега. В нашем случае текста ни в одном теге нет.
print(xmlfile.find('./publication').text)

# Возвращает карту
print(xmlfile.find('./publication').attrib)

map = dict(xmlfile.find('./publication').attrib)
print(map["type"])

# Обращение к атрибуту
print(xmlfile.find('./folder').get('name'))

# Получить название тега
print(xmlfile.find('./folder').tag)

print('---')

# Проход по элементам
for publ in xmlfile.getroot():
    print(publ.get('name'))

print('---')

# Проход по элементам
for publ in xmlfile.getroot().iter('publication'):
    print(publ.get('name'))


s = {"sss","aaa"}

print("ssss" in s)