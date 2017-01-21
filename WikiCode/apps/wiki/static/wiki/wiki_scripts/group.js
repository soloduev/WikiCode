/*
 Copyright (C) 2016-2017 Igor Soloduev <diahorver@gmail.com>

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

$("#jstree")
// listen for event
    .on('changed.jstree', function (e, data) {
        var full_path = '' + data.selected;

        if((''+full_path).split(":")[0] == "publ")
        {
            $("#preview-publ-path").val(full_path);

            $.ajax({
                type: "GET",
                url: "get_path_to_publ/",
                data: {
                    'id_publ': ('' + full_path).split(":")[1],
                },
                dataType: "text",
                cache: false,
                success: function (data) {
                    if (data != 'no') {
                        $("#preview-publ-path-show").val(data);
                    }
                    else {
                        console.log("Не удалось получить полный путь к папке!");
                    }
                }
            });
        }
        else
        {
            $("#preview-publ-path").val("");
            $("#preview-publ-path-show").val("");
        }
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

//Просмотр текущей папки группы, для выбора превью конспекта
$("#choose-preview-publ-btn").click(function () {
    $("#div-choose-preview-publ-group").fadeIn(500);
});

$("#close-choose-preview-publ-group").click(function () {
    $("#div-choose-preview-publ-group").fadeOut(500);
});

$('#preview-publ-path-show').keydown(function(e){
  e.preventDefault()
});

// Работа с настройками конспекта
$('#show-status-group').switchable();
$('#show-description-group').switchable();
$('#show-tags-group').switchable();
$('#show-total-publs-group').switchable();
$('#show-total-members-group').switchable();
$('#show-rating-group').switchable();
$('#show-date-group').switchable();
$('#show-conents-group').switchable();
$('#show-preview-tree-group').switchable();
$('#show-members-group').switchable();
