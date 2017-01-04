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
        var full_path = '' + data.selected;
        $("#save-publ-path-folder").val(full_path);
    })
    // create the instance
    .jstree({

        "types": {
            "folder": {
                "icon": "glyphicon glyphicon-folder-open"
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

        "plugins": ["wholerow", "types"]
    });

(function ($) {
    $(document).ready(function () {
        var mySlidebars = new $.slidebars();
        $('#pollSlider-button').on('click', function () {
            mySlidebars.slidebars.open('left');
            $("#left-slidebar-publications").show();
            $("#left-slidebar-contents").hide();
        });
        $('#contents-pollSlider-button').on('click', function () {
            mySlidebars.slidebars.open('left');
            $("#left-slidebar-contents").show();
            $("#left-slidebar-publications").hide();
        });
    });
})(jQuery);

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
        data: {
            'dynamic_comment': dynamic_comment,
            'num_paragraph': num_paragraph
        },
        dataType: "text",
        cache: false,
        success: function (data) {
            if (data == 'ok') {
                // Чисто с точки зрения фронтенда, добавляем этот комментарий, чтобы не делать дополнительный гет запрос.
                // Либо сделать гет запрос)
                location.reload();
            }
            else {
                console.log("ERROR in page.js");
            }
        }
    });
});


//Динамическое редактирование
$("#edit_paragraph_wiki_tree_context").on("click", function () {

    isEdit = true;
    var selected_num_paragraph = parseInt($("#selected_number_paragraph").val());
    //Получаем все необходимые данные с абазаца
    var height = $('#li-md-wikicode-' + selected_num_paragraph + '').css('height');
    selectText = md_text[parseInt(selected_num_paragraph)];

    //Заменяем элемент списка на input
    $("#markdown-row-" + selected_num_paragraph + "")
        .replaceWith(
            '<textarea  class="form-control dyn-par" id="dynamic-paragraph"' +
            'onKeyUp="selectChange()"' +
            'style="height:' + height + ';' +
            '">' +
            selectText +
            '</textarea>');

    // Делаем так, чтобы все textarea могли автоматически изменять свой размер в зависимости от их содержимого
    $(function () {
        $('textarea').autoResize();
    });

    //Делаем так, чтобы мы могли нажимать таб у любого текст ареа тега
    var textareas = document.getElementsByTagName('textarea');
    var count = textareas.length;
    for (var i = 0; i < count; i++) {
        textareas[i].onkeydown = function (e) {
            if (e.keyCode == 9 || e.which == 9) {
                e.preventDefault();
                var s = this.selectionStart;
                this.value = this.value.substring(0, this.selectionStart) + "\t" + this.value.substring(this.selectionEnd);
                this.selectionEnd = s + 1;
            }
        }
    }
    $(".dyn-par").focus();

    //Устанвливаем курсор в конец строки
    var input = document.getElementById("dynamic-paragraph");
    input.selectionStart = input.value.length - 1;


    //Как только теряем фокус:
    $("#dynamic-paragraph").blur(function (e) {

        //Применяем все и возвращаем все обратно
        var new_md_text = $("#dynamic-paragraph").val();
        $("#dynamic-paragraph").replaceWith(
            '<div class="md-hover" id="markdown-row-' + selected_num_paragraph + '"></div>'
        );
        document.getElementById('markdown-row-' + selected_num_paragraph).innerHTML = marked(new_md_text);
        md_text[parseInt(selected_num_paragraph)] = new_md_text;
        isEdit = false;
    });
});

// Событие клика кнопки "ответить на комментарий". Устанавливает id, на какой комментарий необходимо ответить
$('.main-comment-reply').click(function (eventObject) {
    $("#reply_id_user").val('' + this.getAttribute('id_comment'));
});

// Событие клика кнопки "ответить на динамический комментарий". Устанавливает id, на какой комментарий необходимо ответить
$('body').on('click', '.dynamic-comment-reply', function(eventObject) {
    $("#reply_comment_id_dynamic").val('' + this.getAttribute('id_comment'));
});

// Событие клика кнопки "оставить комментарий". Устанавливает id, на какой комментарий необходимо ответить -1.
$('#wiki-style-btn-send-main-comment').click(function (eventObject) {
    $("#reply_id_user").val('-1');
});

// Отправление ответа на динамический комментарий
$("#wiki-btn-send-dynamic-comment-reply").click(function () {
    // Получаем сообщение которое необходимо отправить
    var comment = $("#wiki-dynamic-comment-field-reply").val();

    // Получаем id того комментария, которому произошел ответ
    var reply_comment_id = $("#reply_comment_id_dynamic").val();

    // Получаем номер параграфа в котором пользователь хочет оставить комментарий
    var num_paragraph = $("#selected_number_paragraph").val();

    $.ajax({
        type: "POST",
        url: "reply_dynamic_comment/",
        data: {
            'comment': comment,
            'reply_comment_id': reply_comment_id,
            'num_paragraph': num_paragraph
        },
        dataType: "text",
        cache: false,
        success: function (data) {
            if (data == 'ok') {
                // Чисто с точки зрения фронтенда, добавляем этот комментарий, чтобы не делать дополнительный гет запрос.
                // Либо сделать гет запрос))
                location.reload();
            }
            else {
                console.log("ERROR in page.js. reply_dynamic_comment()");
            }
        }
    });
});

// Отправление общего комментария
$("#wiki-btn-send-main-comment").click(function () {

    // Получаем сообщение которое необходимо отправить
    var main_comment = $("#wiki-main-comment-field").val();

    // Получаем id того комментария, которому произошел ответ
    var reply_author_id = $("#reply_id_user").val();

    $.ajax({
        type: "POST",
        url: "add_main_comment/",
        data: {
            'main_comment': main_comment,
            'reply_author_id': reply_author_id,
        },
        dataType: "text",
        cache: false,
        success: function (data) {
            if (data == 'ok') {
                // Чисто с точки зрения фронтенда, добавляем этот комментарий, чтобы не делать дополнительный гет запрос.
                // Либо сделать гет запрос))
                location.reload();
            }
            else {
                console.log("ERROR in page.js. Add_main_comment()");
            }
        }
    });
});

// Сохранение изменений в конспекте
$("#wiki-style-btn-save-publ").click(function () {


    var myMap = {};
    for (var i = 1; i < md_text.length; i++) {
        myMap[i.toString()] = md_text[i];
    }

    myMap["count_paragraphs"] = (md_text.length - 1).toString();
    $.ajax({
        type: "POST",
        url: "save_publication/",
        data: myMap,
        dataType: "text",
        cache: false,
        success: function (data) {
            if (data == 'eq') {
                //location.reload();
            }
            else if (data == 'not_eq') {
                location.reload();
            }
            else {
                console.log("ERROR in page.js. Save publ");
            }
        }
    });
});
//
// Установление head версии
$("#set_head_version").click(function () {
    var to_version_str = $("#to_version_value").val();
    if (to_version_str === "") {
    }
    else {
        $.ajax({
            type: "POST",
            url: "set_head/",
            data: {
                "to_version": to_version_str,
            },
            dataType: "text",
            cache: false,
            success: function (data) {
                if (data == 'ok') {
                    location.reload();
                }
                else if (data == 'auth') {
                    location.href = "/login/";
                }
                else {
                    console.log("ERROR in page.js. Set HEAD Version.");
                }
            }
        });
    }

});

//Просмотр папок, для определения той, в которой хотим сохранить конспект
$("#set-path-folder-save").click(function () {
    $("#div-choose-folder-save").fadeIn(500);
});

$("#close-choose-folder-path").click(function () {
    $("#div-choose-folder-save").fadeOut(500);
});