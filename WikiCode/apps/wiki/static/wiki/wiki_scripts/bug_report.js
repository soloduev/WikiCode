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


//Подтверждение удаления конспекта в дереве сохраненых конспектов
$("#wiki-style-btn-add-bug").click(function () {

    if($("#message_input_error").val().length > 50)
    {

        $.ajax({
            type: "POST",
            url: "send_bug/",
            data:{
                'text':''+$("#message_input_error").val(),
            },
            dataType: "text",
            cache: false,
            success: function(data){
                if (data == 'ok'){
                    //location.reload();
                    console.log("Отправлено");
                    $("#wiki_send_bug_report").attr("style", "display:none;");
                    $("#wiki_sended_bug_report").attr("style", "");
                }
            }
        });
    }
    else
    {
        console.log("В сообщении должно быть больше 50 символов");
    }


});