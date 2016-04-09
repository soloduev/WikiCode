/**
 * Created by Igor on 09.04.2016.
 */

$.jstree.defaults.core.themes.variant = "large";

var selected_file_in_tree = "NONE_SELECT";
var adding_folder_to = "NONE";

$("#jstree")
// listen for event
    .on('changed.jstree', function (e, data) {
        selected_file_in_tree = data.selected;
        if(adding_folder_to !== "NONE" && adding_folder_to != selected_file_in_tree)
        {
            $("#div_folder_name_input").attr("style", "display: none;");
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





