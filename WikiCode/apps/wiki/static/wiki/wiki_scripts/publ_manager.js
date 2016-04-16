/**
 * Created by lazytroll on 16.04.16.
 */


//Подтверждение удаления конспекта
$("#wiki-style-btn-delete-publ").click(function () {
    var title_publ = $("#myModalLabelTitlePublication").val();

        $.ajax({
            type: "GET",
            url: "delete_publ_in_tree/",
            data:{
                'answer':title_publ,
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