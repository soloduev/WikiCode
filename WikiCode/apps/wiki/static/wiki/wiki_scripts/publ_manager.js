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
 * Created by lazytroll on 16.04.16.
 */


//Подтверждение удаления конспекта
$("#wiki-style-btn-delete-publ").click(function () {
    var title_publ = $("#myModalLabelTitlePublication").val();

    $.ajax({
        type: "POST",
        url: "delete_publ_in_tree/",
        data:{
            'answer':title_publ,
        },
        dataType: "text",
        cache: false,
        success: function(data){
            if (data == 'ok'){
                location.href = '/tree_manager/';
            }
            else{
                console.log("ERROR in publ_manager.js");
            }
        }
    });
});

var correct_nickname = false;

//GET запрос на проверку, существования пользователя для назначения его редактором конспекта
$("#input-for-add-editor").on("input",function () {

    //Отправляем ajax запрос на сервер
    $.ajax({
        type: "GET",
        url: "check_nickname_for_add_editor/",
        data:{
            'nickname':$("#input-for-add-editor").val(),
            'id_publ_for_add_editor':$("#id_publ_for_add_editor").val(),
        },
        dataType: "text",
        cache: false,
        success: function(data){
            if (data == 'ok'){
                $("#info-message-for-add-editor").text("");
                correct_nickname = true;
            }
            else if(data == "author")
            {
                $("#info-message-for-add-editor").text("Вы и так являетесь автором данного конспекта");
                $("#info-message-for-add-editor").attr("style","color: red;");
                correct_nickname = false;
            }
            else
            {
                $("#info-message-for-add-editor").text("Такого пользователя не существует!");
                $("#info-message-for-add-editor").attr("style","color: red;");
                correct_nickname = false;
            }
        }
    });
});

//Реакция на кнопку модального окна назначения нового пользователя редактором, "назначить"
$("#wiki-style-btn-add-editor").on('click', function () {
    //Добавление значение input
    if(correct_nickname == true)
    {
        //Отправляем ajax запрос на сервер
        $.ajax({
            type: "POST",
            url: "add_editor/",
            data:{
                'nickname':$("#input-for-add-editor").val(),
                'id_publ_for_add_editor':$("#id_publ_for_add_editor").val(),
            },
            dataType: "text",
            cache: false,
            success: function(data){
                if (data == 'ok'){
                    location.href = ""+$("#id_publ_for_add_editor").val();
                }
                else
                {

                }
            }
        });
    }
});
