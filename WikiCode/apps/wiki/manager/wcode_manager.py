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


# Менеджер управления сайтом.
# Максимально продвинутое и удобное управление сайтом

import subprocess, os, sys, datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import configuration
from WikiCode.apps.wiki.src.wiki_tests import WikiTests


# Главный обработчик команд
def execute_commands(args):
    commands = args[2:]
    count_commands = len(commands)
    if count_commands == 0:
        print("Вы не ввели ни одну команду.")
        __print_help()
    elif count_commands == 1:
        if commands[0] == "install":
            __install_wikicode()
        elif commands[0] == "clearall":
            __clear_wikicode()
        elif commands[0] == "test":
            __test_wikicode()
    elif count_commands == 2:
        if commands[0] == "load":
            __load_db(commands[1])


# Очищает текущее состояние сайта и запускает его с самого начала
def __install_wikicode():

    print("Installing new wikicode database:")
    __backup_current_database()
    #subprocess.call(["python3", "manage.py", "flush"])
    #subprocess.call(["python3", "manage.py", ])


# Очищает текущее состояние сайта
def __clear_wikicode():

    print("Clearing wikicode database...")
    __backup_current_database()
    subprocess.call(["python3", "manage.py", "flush"])


def __backup_current_database():
    # Получаем текущую дату
    date = str(datetime.datetime.now())
    date = date[:len(date) - 7]

    # Составляем имя файла, в котором будет бекап текущей БД
    backup_file_name = configuration.BACKUP_FILE_NAME + "_" + str(date) + "." + configuration.BACKUP_FILE_FORMAT
    backup_file_name = backup_file_name.replace(" ", "_")
    print("Backup creating...")

    # Делаем сам бекап
    subprocess.call(["python3", "manage.py", "dumpdata", "--natural-foreign",
                     "-e", "sessions", "-e", "admin", "-e", "contenttypes",
                     "-e", "auth.Permission", "--format="+configuration.BACKUP_FILE_FORMAT,
                     "--indent="+str(configuration.BACKUP_FILE_INDENT),
                     "--output="+backup_file_name])

    # Отпрaвляем полученный файл на почту
    print("Backup sending...")
    __send_mail(configuration.EMAIL_BACKUP_SENDER_NAME,
                configuration.EMAIL_BACKUP_RECEIVER_NAME,
                configuration.EMAIL_BACKUP_SUBJECT,
                configuration.EMAIL_BACKUP_TEXT,
                backup_file_name)

    # Затем удаляем этот файл
    print("Remove files...")
    os.remove(backup_file_name)


def __load_db(db_filename):
    assert os.path.isfile(db_filename), "Database file not exist"

    print("Loading database file for wikicode:")
    __backup_current_database()
    print("Load new file...:")
    subprocess.call(["python3", "manage.py", "loaddata", db_filename])


def __test_wikicode():
    wiki_tests = WikiTests()
    is_errors = wiki_tests.run()

def __print_help():
    print("Справка по командам сайта:")
    print("install          -   первая настоящая установка сайта")
    print("present          -   первая установка сайта с набором тестовых данных")
    print("clearall         -   очищает всю БД и все данные")
    print("load <filename>  -   загружает определенную версию БД сайта")
    print("help             -   выводит справку по командам сайта")


def __send_mail(send_from, send_to, subject, text, filename):

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = send_to

    # The main body is just another attachment
    body = MIMEText(text)
    msg.attach(body)

    # PDF attachment
    fp = open(filename, 'rb')
    att = MIMEApplication(fp.read(), _subtype="xml")
    fp.close()
    att.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(att)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(send_from, configuration.EMAIL_BACKUP_SENDER_PASSWORD)
    server.sendmail(send_from, [send_to], msg.as_string())
    server.close()
