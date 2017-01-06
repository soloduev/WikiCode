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
    var id_publ = $("#myModalLabelTitlePublication").val();

    $.ajax({
        type: "POST",
        url: "delete_publ_in_tree/",
        data:{
            'id_publ':id_publ,
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

// Работа с настройками конспекта
$('#access-switch').switchable();
$('#dynamic-switch').switchable();
$('#main-comments-switch').switchable();
$('#private-edit-switch').switchable();
$('#contents-switch').switchable();
$('#files-switch').switchable();
$('#links-switch').switchable();
$('#versions-switch').switchable();
$('#show-author-switch').switchable();
$('#loading-switch').switchable();
$('#saving-switch').switchable();
$('#rating-switch').switchable();
$('#file-tree-switch').switchable();
