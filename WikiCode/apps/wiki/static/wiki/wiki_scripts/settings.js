/*
 Copyright (C) 2016 Igor Soloduev <diahorver@gmail.com>

 This file is part of WikiCode.

 WikiCode is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 WikiCode is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with WikiCode.  If not, see <http://www.gnu.org/licenses/>.
 */


// Здесь, по мимо встроенной валидации форм, проводим валидацию с помощью js.
// Если все успешно, возвращаем true, иначе, если не успешно, указываем поле которое не верно, а затем возвращаем false.
function validate_repassword_form(){
    // Получаем все данные с полей формы
    old_password = $("#old_password_input").val();
    password = $("#user_password_input").val();
    repeat_password = $("#user_password_repeat_input").val();

    // Теперь регексуем, проверяем на правильность введенных данных через регексы
    is_correct_old_password = /[a-zA-Z0-9]{6,16}/.test(old_password);
    is_correct_password = /[a-zA-Z0-9]{6,16}/.test(password);
    is_correct_password_repeat = /[a-zA-Z0-9]{6,16}/.test(repeat_password);
    is_passwords_equals = (password === repeat_password);

    // Если все ок, двигаемся дальше
    if(is_correct_old_password && is_correct_password && is_correct_password_repeat)
    {
        is_submit = false;

        // Теперь выполняем гет запросы на существование никнейма и почты
        // Отправляем ajax запрос на сервер c целью узнать, правильный ли пароль ввел текущий пользоаватель
        $.ajax({
            type: "GET",
            url: "check_password/",
            data: {
                'password': ""+old_password,
            },
            dataType: "text",
            cache: false,
            success: function (data) {
                if (data == 'ok') {
                    is_submit = true;
                }
                else {
                    alert("Вы ввели не правильный старый пароль!");
                }
            },
            async: false
        });

        return is_submit;
    }
    else
    {
        // Если нет, то указываем причину неправильно введенных данных

        if(!is_passwords_equals)
        {
            alert("Пароли должны совпадать");
        }
        else if(!is_correct_password_repeat || !is_correct_password || is_correct_old_password)
        {
            alert("Пароль должен состоять только из букв латинского алфавита и цифр. Его длина должна находиться в диапазоне от 6 до 16 символов.");
        }

        return false;
    }
}