$.fn.extend({
    treed: function (o) {

        var openedClass = 'glyphicon-minus-sign';
        var closedClass = 'glyphicon-plus-sign';

        if (typeof o != 'undefined'){
            if (typeof o.openedClass != 'undefined'){
                openedClass = o.openedClass;
            }
            if (typeof o.closedClass != 'undefined'){
                closedClass = o.closedClass;
            }
        };

        //initialize each of the top levels
        var tree = $(this);
        tree.addClass("tree");
        tree.find('li').has("ul").each(function () {
            var branch = $(this); //li with children ul
            branch.prepend("<i class='indicator glyphicon " + closedClass + "'></i>");
            branch.addClass('branch');
            branch.on('click', function (e) {
                if (this == e.target) {
                    var icon = $(this).children('i:first');
                    icon.toggleClass(openedClass + " " + closedClass);
                    $(this).children().children().toggle();
                }
            })
            branch.children().children().toggle();
        });
        //fire event from the dynamically added icon
        tree.find('.branch .indicator').each(function(){
            $(this).on('click', function () {
                $(this).closest('li').click();
            });
        });
        //fire event to open branch if the li contains an anchor instead of text
        tree.find('.branch>a').each(function () {
            $(this).on('click', function (e) {
                $(this).closest('li').click();
                e.preventDefault();
            });
        });
        //fire event to open branch if the li contains a button instead of text
        tree.find('.branch>button').each(function () {
            $(this).on('click', function (e) {
                $(this).closest('li').click();
                e.preventDefault();
            });
        });
    }
});

//Initialization of treeviews

$('#tree1').treed();

$('#tree2').treed({openedClass:'glyphicon-folder-open', closedClass:'glyphicon-folder-close'});

$('#tree3').treed({openedClass:'glyphicon-chevron-right', closedClass:'glyphicon-chevron-down'});



//Кусок скрипта относится к странице tree_manager.html
//-------------------------------------------------

$(document).ready(function () {
    $.getScript("http://code.jquery.com/ui/1.9.2/jquery-ui.js").done(function (script, textStatus) { $('tbody').sortable();$(".alert-info").alert('close');$(".alert-success").show(); });
});


//-------------------------------------------------

//Этот кусок скрипта относится к форме регистрации пользователей
//-------------------------------------------------

//Проверка имени пользователя

$("#wiki_nickname").on("change", function () {
    if($("#wiki_nickname").val().length < 3 && $("#wiki_nickname").val() !== "")
    {
        $("#wiki_nickname_message").text("Nickname должен быть от 3 до 12 символов");
        $("#wiki_nickname_message").attr("style","color: red;");
    }
    else if($("#wiki_nickname").val() === "")
    {
        $("#wiki_nickname_message").text("Your Nickname");
        $("#wiki_nickname_message").attr("style","color: black;");
    }
    else
    {
        $("#wiki_nickname_message").text("Your Nickname");
        $("#wiki_nickname_message").attr("style","color: black;");
        //Отправляем ajax запрос на сервер
        $.ajax({
            type: "GET",
            url: "check_nickname/",
            data:{
                'nickname':$("#wiki_nickname").val(),
            },
            dataType: "text",
            cache: false,
            success: function(data){
                if (data == 'ok'){
                    $("#wiki_nickname_message").text("Такой Nickname уже существует!");
                    $("#wiki_nickname_message").attr("style","color: red;");
                }
                else
                {
                    $("#wiki_nickname_message").text("Correct Nickname!");
                    $("#wiki_nickname_message").attr("style","color: green;");
                }
            }
        });
    }
});

//Проверка почты пользователя

$("#wiki_email").on("change", function () {

    $("#wiki_email_message").text("Your Email");
    $("#wiki_email_message").attr("style","color: black;");
    //Отправляем ajax запрос на сервер
    $.ajax({
        type: "GET",
        url: "check_email/",
        data:{
            'email':$("#wiki_email").val(),
        },
        dataType: "text",
        cache: false,
        success: function(data){
            if (data == 'ok'){
                $("#wiki_email_message").text("Такой Email уже существует!");
                $("#wiki_email_message").attr("style","color: red;");
            }
        }
    });

});


//-------------------------------------------------