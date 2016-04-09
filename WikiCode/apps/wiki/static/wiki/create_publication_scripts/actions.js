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

