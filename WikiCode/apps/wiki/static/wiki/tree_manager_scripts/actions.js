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

        "plugins" : [ "wholerow", "types" ]
    });

//Добавление папки в дерево
$("#add_folder_in_wiki_tree").click(function () {

    if(selected_file_in_tree !== "NONE_SELECT")
    {
        $("#div_folder_name_input").attr("style", "");
        $("#panel_inputs").attr("style", "display: none;");
        adding_folder_to = selected_file_in_tree
    }
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
            type: "GET",
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
        $("#div_accept_delete_elem").attr("style", "");
        $("#panel_inputs").attr("style", "display: none;");
        var str = ''+selected_file_in_tree;
        var arr = str.split(":");
        $("#deleter-text-tree-manager").text("Delete "+arr[0]+" ?");
        adding_folder_to = selected_file_in_tree;
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
        $.ajax({
            type: "GET",
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

});


