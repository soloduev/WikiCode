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

//Динамический конспект

