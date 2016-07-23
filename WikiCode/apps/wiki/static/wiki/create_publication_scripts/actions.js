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
 * Created by Igor on 09.04.2016.
 */

$("#jstree")
// listen for event
    .on('changed.jstree', function (e, data) {
        var full_path = ''+data.selected;
        var arr = full_path.split(':');
        $("#lt-markdown-folder").val(arr[0]);
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



//Просмотр папок, для определения той, в которой хотим создать конспект
$("#lt-markdown-set-path").click(function () {

    //$("#div-lt-choose-folder").attr("style", "");
    $("#div-lt-choose-folder").fadeIn(500);
    //$("#div-lt-choose-folder").fadeOut(1000);
});

$("#lt-markdown-close-choose").click(function () {
    $("#div-lt-choose-folder").fadeOut(500);
});

// Работа с настройками конспекта
$('#access-switch').switchable();
$('#dynamic-switch').switchable();
$('#main-comments-switch').switchable();
$('#private-edit-switch').switchable();
$('#contents-switch').switchable();
$('#files-switch').switchable();
$('#links-switch').switchable();
$('#versions-switch').switchable();