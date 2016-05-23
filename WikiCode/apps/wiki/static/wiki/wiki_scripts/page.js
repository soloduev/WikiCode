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


//Добавление комментария к конспекту
$("#wiki-style-btn-add-comment").click(function () {

    if(($("#add-comment-wiki-page").val().length >=10))
    {
        comment_message = $("#add-comment-wiki-page").val();
        $.ajax({
            type: "POST",
            url: "add_comment_in_wiki_page/",
            data:{
                'comment_message':''+comment_message,
            },
            dataType: "text",
            cache: false,
            success: function(data){
                if (data == 'ok'){
                    location.reload();
                }
                else
                {
                    //Говорим, что комментарий добавить не удалось(
                }
            }
        });
    }
});

//Лайк конспекта
$("#wikicode-like-publ").click(function () {
    $.ajax({
        type: "POST",
        url: "like_wiki_page/",
        data:{
            'data':'',
        },
        dataType: "text",
        cache: false,
        success: function(data){
            if (data == 'ok'){
                location.reload();
            }
            else
            {
                //Говорим, что лайкнуть не удалось(
            }
        }
    });
});

//Сохранение конспекта
$("#wiki-style-btn-save-publ").click(function () {
    var path_folder = $("#save-publ-path-folder").val()
    if(path_folder !== "")
    {
        $.ajax({
            type: "POST",
            url: "import_wiki_page/",
            data:{
                'path_folder':''+path_folder,
            },
            dataType: "text",
            cache: false,
            success: function(data){
                if (data == 'ok'){
                    location.href = '/tree_manager';
                }
                else
                {

                }
            }
        });
    }

});

//Ответ на общий комментарий
$("#wiki-send-comment-answer").click(function () {
    if($("#input_wiki_comment_answer").val().length > 10)
    {
        $.ajax({
            type: "POST",
            url: "send_answer_comment/",
            data:{
                'nickname':''+$("#nickname-comment-message-for-answer").val(),
                'text':''+$("#text-comment-message-for-answer").val(),
                'answer':''+$("#input_wiki_comment_answer").val(),
            },
            dataType: "text",
            cache: false,
            success: function(data){
                if (data == 'ok'){
                    location.reload();
                }
                else
                {

                }
            }
        });
    }
    else
    {
        console.log("Текст ответа на общий комментарий должен быть длиннее 10 символов");
    }
});

//Все что касается динамики далее


function selectChange() {
    selectText = $("#dynamic-paragraph").val();
};

//Динамическое редактирование
$("#wiki-style-btn-option-1").on("click", function () {

    isEdit = true;
    //Получаем все необходимые данные с абазаца
    var height = $('#li-md-wikicode-'+num_paragraph+'').css('height');
    selectText = md_text[parseInt(num_paragraph)];

    //Заменяем элемент списка на input
    $("#markdown-row-"+num_paragraph+"")
        .replaceWith(
            '<textarea class="form-control dyn-par" id="dynamic-paragraph"' +
            'onKeyUp="selectChange()"' +
            'style="height:'+height+';' +
            '">' +
            selectText +
            '</textarea>');
    $(".dyn-par").focus();

    //Как только теряем фокус:
    $("#dynamic-paragraph").blur(function (e) {

        //Применяем все и возвращаем все обратно
        $("#dynamic-paragraph").replaceWith(
            '<div class="md-hover" id="markdown-row-'+num_paragraph+'"></div>'
        );
        document.getElementById('markdown-row-'+num_paragraph).innerHTML = marked(selectText);
        md_text[parseInt(num_paragraph)] = selectText;
        isEdit = false;
        update_comment_marks();
    });
});

$(document).mouseup(function()
{
    $("#context-dinamic-menu").hide();
});

$(document).mouseleave(function () {
    $("#context-dinamic-menu").hide();
});

$(document).scroll(function () {
    $("#context-dinamic-menu").hide();
});

$(window).resize(function () {
    $("#context-dinamic-menu").hide();
    update_comment_marks();
});



$("#wiki-style-btn-option-2").on('click', function () {
    document.getElementById('paragraph_input_error').innerHTML = marked(md_text[num_paragraph]);
});

$("#wiki-style-btn-option-3").on('click', function () {
    document.getElementById('paragraph_input_md_paragraph').innerHTML = marked(md_text[num_paragraph]);
    var insert_data =  $("#dynamic-comment-paragraph-"+num_paragraph).html();
    if(insert_data !== undefined)
        $("#paragraph_input_comment").html(insert_data);
    else{
        $("#paragraph_input_comment").html("<h4>Комментариев к этому блоку пока нет. Станьте первым!</h4>");
    }
});

//То что касается тегов
$(function() {
    $('#publ-tags').tags({
        readOnly: true,
        tagData:["c++", "beginning"],
    });
});

/*Ajax запрос на добавления комментария*/
//Добавление комментария к конспекту
$("#wiki-style-btn-add-dynamic-comment").click(function () {
    comment_message = $("#wiki-input-dynamic-comment").val();
    $.ajax({
        type: "POST",
        url: "add_dynamic_comment_in_wiki_page/",
        data:{
            'comment_message':''+comment_message,
            'num_paragraph':''+num_paragraph,
        },
        dataType: "text",
        cache: false,
        success: function(data){
            if (data == 'ok'){
                location.reload();
            }
            else
            {
                //Говорим, что комментарий добавить не удалось(
            }
        }
    });
});


//Переключение вкладок
$("#wiki-publ-tab-1").on("click", function () {
    $(".wikicode-commenting-mark").show();
});
$("#wiki-publ-tab-2").on("click", function () {
    $(".wikicode-commenting-mark").hide();
});
$("#wiki-publ-tab-3").on("click", function () {
    $(".wikicode-commenting-mark").hide();
});
$("#wiki-publ-tab-4").on("click", function () {
    $(".wikicode-commenting-mark").hide();
});
$("#wiki-publ-tab-5").on("click", function () {
    $(".wikicode-commenting-mark").hide();
});
$("#wiki-publ-tab-6").on("click", function () {
    $(".wikicode-commenting-mark").hide();
});
$("#wiki-publ-tab-7").on("click", function () {
    $(".wikicode-commenting-mark").hide();
});



