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

//Использование POST запроса в AJAX и DJANGO
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



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
            type: "GET",
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
        type: "GET",
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
                //Говорим, что лайкнуть не удалось(
            }
        }
    });
    }

});

