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

$.jstree.defaults.core.themes.variant = "large";

var selected_file_in_tree = "NONE_SELECT";
var adding_folder_to = "NONE";
$("#choose-folder-secret").val("NONE");

$("#jstree")
// listen for event
    .on('changed.jstree', function (e, data) {
        selected_file_in_tree = data.selected;
        $("#choose-folder-secret").val(selected_file_in_tree);
        if(adding_folder_to !== "NONE" && adding_folder_to != selected_file_in_tree)
        {
            $("#div_folder_name_input").attr("style", "display: none;");
            $("#div_accept_delete_elem").attr("style", "display: none;");
            $("#div_rename_publ_input").attr("style", "display: none;");
            $("#div_rename_folder_input").attr("style", "display: none;");
            $("#panel_inputs").attr("style", "");
        }

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


        "plugins" : [ "wholerow", "types"],

        "core" : {
            "multiple" : false,
        },
    });

//Добавление папки в дерево
$("#add_folder_in_wiki_tree").click(function () {

    if(selected_file_in_tree !== "NONE_SELECT")
    {
        if((''+selected_file_in_tree).indexOf(".publ") != -1)
        {

        }
        else
        {
            $("#div_folder_name_input").attr("style", "");
            $("#panel_inputs").attr("style", "display: none;");
            adding_folder_to = selected_file_in_tree
        }
    }
});

//Добавление папки в дерево из контекстного меню
$("#add_folder_in_wiki_tree_context").click(function () {

    if(selected_file_in_tree !== "NONE_SELECT")
    {

        $("#div_folder_name_input").attr("style", "");
        $("#panel_inputs").attr("style", "display: none;");
        adding_folder_to = selected_file_in_tree

    }
});

//Удаление папки из дерева из контекстного меню
$("#delete_folder_in_wiki_tree_context").click(function () {

    if(selected_file_in_tree !== "NONE_SELECT")
    {
        if((''+selected_file_in_tree).indexOf(".publ") != -1)
        {

        }
        else
        {
            //Далее проверка, есть ли конспекты в папке:

            $.ajax({
                type: "POST",
                url: "check_folder_for_delete/",
                data:{
                    'answer':''+selected_file_in_tree,
                },
                dataType: "text",
                cache: false,
                success: function(data){
                    if (data == 'ok'){
                        $("#div_accept_delete_elem").attr("style", "");
                        $("#panel_inputs").attr("style", "display: none;");
                        var str = ''+selected_file_in_tree;
                        var arr = str.split(":");
                        $("#deleter-text-tree-manager").text("Delete "+arr[0]+" ?");
                        adding_folder_to = selected_file_in_tree;
                    }
                    else
                    {
                        //Говорим, что удалять можно только пустые папки
                    }
                }
            });
        }
    }
});

//Создание конспекта в выбранной папке из контекстного меню
$("#create_publ_in_wiki_tree_context").click(function () {
    $("#add_publ_in_wiki_tree").click();
});


//Отмена добавления папки в дерево
$("#cancel_add_folder_in_wiki_tree").click(function () {
    $("#div_folder_name_input").attr("style", "display: none;");
    $("#panel_inputs").attr("style", "");
    adding_folder_to = "NONE";
});


//Подтверждение добавления папки в дерево
$("#accept_add_folder_in_wiki_tree").click(function () {

    new_folder_name = $("#folder_name_input").val();

    if(new_folder_name !== "")
    {
        $.ajax({
            type: "POST",
            url: "add_folder_in_tree/",
            data:{
                'answer':new_folder_name+"^^^"+selected_file_in_tree,
            },
            dataType: "text",
            cache: false,
            success: function(data){
                if (data == 'ok'){
                    location.reload();
                }
            }
        });
    }
});

//Удаление элемента из дерева
$("#del-element-in-tree").click(function () {

    if(selected_file_in_tree !== "NONE_SELECT")
    {
        if((''+selected_file_in_tree).indexOf(".publ") != -1)
        {

        }
        else
        {
            //Далее проверка, есть ли конспекты в папке:

            $.ajax({
                type: "POST",
                url: "check_folder_for_delete/",
                data:{
                    'answer':''+selected_file_in_tree,
                },
                dataType: "text",
                cache: false,
                success: function(data){
                    if (data == 'ok'){
                        $("#div_accept_delete_elem").attr("style", "");
                        $("#panel_inputs").attr("style", "display: none;");
                        var str = ''+selected_file_in_tree;
                        var arr = str.split(":");
                        $("#deleter-text-tree-manager").text("Delete "+arr[0]+" ?");
                        adding_folder_to = selected_file_in_tree;
                    }
                    else
                    {
                        //Говорим, что удалять можно только пустые папки
                    }
                }
            });
        }
    }

});


//Отмена удаления
$("#no_delete_elem_in_tree").click(function () {
    $("#div_accept_delete_elem").attr("style", "display: none;");
    $("#panel_inputs").attr("style", "");
    adding_folder_to = "NONE";
});


//Подтверждение удаления элемента
$("#yes_delete_elem_in_tree").click(function () {

    if(selected_file_in_tree !== "NONE_SELECT")
    {
        if((''+selected_file_in_tree).indexOf(".publ") != -1)
        {

        }
        else
        {
            $.ajax({
                type: "POST",
                url: "del_elem_in_tree/",
                data:{
                    'answer':''+selected_file_in_tree,
                },
                dataType: "text",
                cache: false,
                success: function(data){
                    if (data == 'ok'){
                        location.reload();
                    }
                }
            });
        }
    }

});


//Открыть конспект. Действие их контекстного меню
$("#open_publ_in_wiki_tree_context").click(function () {
    var tree_path_str = ''+selected_file_in_tree;
    var arr = tree_path_str.split(':');
    var id = ''+arr[1];
    location.href = '/page/'+id;
});

//Открыть настройки конспекта(панель управления конспектом) из контекстного меню
$("#open_settings_publ_in_wiki_tree_context").click(function () {
    var tree_path_str = ''+selected_file_in_tree;
    var arr = tree_path_str.split(':');
    var id = ''+arr[1];
    location.href = '/publ_manager/'+id;
});

//Переименовать конспект из контекстного меню
$("#rename_publ_in_wiki_tree_context").click(function () {
    if(selected_file_in_tree !== "NONE_SELECT") {
        if (('' + selected_file_in_tree).indexOf(".publ") != -1) {
            $("#div_rename_publ_input").attr("style", "");
            $("#panel_inputs").attr("style", "display: none;");
            adding_folder_to = selected_file_in_tree
        }
        else
        {

        }
    }
});

//Отмена переименовывания конспекта
$("#cancel_rename_publ_in_wiki_tree").click(function () {
    $("#div_rename_publ_input").attr("style", "display: none;");
    $("#panel_inputs").attr("style", "");
    adding_folder_to = "NONE";
});

//Подтверждение переименовывания конспекта
$("#accept_rename_publ_in_wiki_tree").click(function () {

    if (selected_file_in_tree !== "NONE_SELECT") {
        if (('' + selected_file_in_tree).indexOf(".publ") != -1) {

            new_name_publ = $("#rename_publ_input").val();
            $.ajax({
                type: "POST",
                url: "rename_publ_in_tree/",
                data:{
                    'answer':''+new_name_publ+"^^^"+selected_file_in_tree,
                },
                dataType: "text",
                cache: false,
                success: function(data){
                    if (data == 'ok'){
                        location.reload();
                    }
                }
            });

        }
        else
        {

        }
    }
});

//Переименовывание папки из контекстного меню
$("#rename_folder_in_wiki_tree_context").click(function () {
    if(selected_file_in_tree !== "NONE_SELECT")
    {
        if((''+selected_file_in_tree).indexOf(".publ") != -1)
        {

        }
        else {
            var name_folder = ('' + selected_file_in_tree).split(":")[0];
            if (name_folder !== "Personal/" && name_folder !== "Imports/")
            {
                $("#div_rename_folder_input").attr("style", "");
                $("#panel_inputs").attr("style", "display: none;");
                adding_folder_to = selected_file_in_tree;
            }

        }


    }
});

//Отмена переименовывания папки
$("#cancel_rename_folder_in_wiki_tree").click(function () {
    $("#div_rename_folder_input").attr("style", "display: none;");
    $("#panel_inputs").attr("style", "");
    adding_folder_to = "NONE";
});


//Подтверждение переименовывания папки
$("#accept_rename_folder_in_wiki_tree").click(function () {

    if (selected_file_in_tree !== "NONE_SELECT") {
        if (('' + selected_file_in_tree).indexOf(".publ") != -1) {


        }
        else
        {
            new_name_folder = $("#rename_folder_input").val();

            $.ajax({
                type: "POST",
                url: "rename_folder_in_tree/",
                data:{
                    'answer':''+new_name_folder+"^^^"+selected_file_in_tree,
                },
                dataType: "text",
                cache: false,
                success: function(data){
                    if (data == 'ok'){
                        location.reload();
                    }
                }
            });

        }
    }
});

//Установление превью-публикации
$("#set_preview_publ_in_wiki_tree_context").click(function () {

    if (selected_file_in_tree !== "NONE_SELECT") {
        if (('' + selected_file_in_tree).indexOf(".publ") != -1) {

            $.ajax({
                type: "POST",
                url: "set_preview_publ_in_tree/",
                data:{
                    'publ':''+selected_file_in_tree,
                },
                dataType: "text",
                cache: false,
                success: function(data){
                    if (data == 'ok'){
                        location.reload();
                    }
                }
            });
        }
        else
        {


        }
    }
});