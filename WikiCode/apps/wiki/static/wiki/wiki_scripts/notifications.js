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



/**
 * Created by lazytroll on 22.05.16.
 */


//Добавление пользователя в коллеги
$("#add_colleague_invite").click(function () {
    $.ajax({
        type: "POST",
        url: "add_colleague/",
        data:{
            'nickname':''+$("#notification-user-invite").text(),
        },
        dataType: "text",
        cache: false,
        success: function(data){
            if (data == 'ok'){
                location.href = "/colleagues";
            }
        }
    });
});

//Удаление уведомления
$("#wiki-style-btn-remove-notification").click(function () {
    console.log();
    console.log();
    $.ajax({
        type: "POST",
        url: "remove_notification/",
        data:{
            'nickname':''+$("#notification-global-nickname").val(),
            'date':''+$("#notification-global-date").val(),
        },
        dataType: "text",
        cache: false,
        success: function(data){
            if (data == 'ok'){
                location.reload();
            }
        }
    });
});