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
 * Created by Igor on 11.04.2016.
 */


$("#jstree")
// listen for event
    .on('changed.jstree', function (e, data) {
        var full_path = ''+data.selected;
        var arr = full_path.split(':');
        $("#save-publ-path-folder").val(arr[0]);
    })
    // create the instance
    .jstree({

        "types" : {
            "folder" : {
                "icon" : "glyphicon glyphicon-folder-open"
            },
            "publ": {
                "icon": "glyphicon glyphicon-list-alt"
            },
            "contents": {
                "icon": "glyphicon glyphicon-bookmark"
            },
            "test": {
                "icon": "glyphicon glyphicon-check"
            },
        },

        "plugins" : [ "wholerow", "types" ]
    });

(function($) {
    $(document).ready(function() {
        var mySlidebars = new $.slidebars();
        $('#pollSlider-button').on('click', function() {
            mySlidebars.slidebars.open('left');
        });
    });
}) (jQuery);

//То что касается тегов
$(function() {
    $('#publ-tags').tags({
        readOnly: true,
        tagData:["c++", "beginning"],
    });
});


// ---------------------------------------------------------- //
// ---------------------POST запросы------------------------- //
// ---------------------------------------------------------- //


// Отправление динамического комментария
$("#wiki-btn-send-dynamic-comment").click(function () {

    // Получаем сообщение которое необходимо отправить
    var dynamic_comment = $("#wiki-dynamic-comment-field").val();

    // Получаем номер параграфа в котором пользователь хочет оставить комментарий
    var num_paragraph = $("#selected_number_paragraph").val();


    $.ajax({
        type: "POST",
        url: "add_dynamic_comment/",
        data:{
            'dynamic_comment':dynamic_comment,
            'num_paragraph':num_paragraph
        },
        dataType: "text",
        cache: false,
        success: function(data){
            if (data == 'ok'){
                // Чисто с точки зрения фронтенда, добавляем этот комментарий, чтобы не делать дополнительный гет запрос.
                // Либо сделать гет запрос)
                location.reload();
            }
            else{
                console.log("ERROR in page.js");
            }
        }
    });
});
