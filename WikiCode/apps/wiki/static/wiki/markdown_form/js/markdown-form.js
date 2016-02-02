/**
 * Created by Igor on 29.01.2016.
 */

jQuery.fn.extend({
    insertAtCaret: function(myValue){
        return this.each(function(i) {
            if (document.selection) {
                // Для браузеров типа Internet Explorer
                this.focus();
                var sel = document.selection.createRange();
                sel.text = myValue;
                this.focus();
            }
            else if (this.selectionStart || this.selectionStart == '0') {
                // Для браузеров типа Firefox и других Webkit-ов
                var startPos = this.selectionStart;
                var endPos = this.selectionEnd;
                var scrollTop = this.scrollTop;
                this.value = this.value.substring(0, startPos)+myValue+this.value.substring(endPos,this.value.length);
                this.focus();
                this.selectionStart = startPos + myValue.length;
                this.selectionEnd = startPos + myValue.length;
                this.scrollTop = scrollTop;
            } else {
                this.value += myValue;
                this.focus();
            }
        })
    }
});


$( init );

function init() {

  $('#lt-markdown-bold').bind( 'click', addBold );
  $('#lt-markdown-italic').bind( 'click', addItalic );
  $('#lt-markdown-ol').bind( 'click', addOl );
  $('#lt-markdown-ul').bind( 'click', addUl );
  $('#lt-markdown-code').bind( 'click', addCode );
  $('#lt-markdown-link').bind( 'click', addLink );
  $('#lt-markdown-line').bind( 'click', addLine );
  $('#lt-markdown-quote').bind( 'click', addQuote );
  $('#lt-markdown-h1').bind( 'click', addH1 );
  $('#lt-markdown-h2').bind( 'click', addH2 );
  $('#lt-markdown-h3').bind( 'click', addH3 );
  $('#lt-markdown-h4').bind( 'click', addH4 );
  $('#lt-markdown-h5').bind( 'click', addH5 );
  $('#lt-markdown-theme1').bind( 'click', addTheme1 );
  $('#lt-markdown-theme2').bind( 'click', addTheme2 );
  $('#lt-markdown-theme3').bind( 'click', addTheme3 );
  $('#lt-markdown-theme4').bind( 'click', addTheme4 );
  $('#lt-markdown-theme5').bind( 'click', addTheme5 );
  $('#lt-markdown-theme6').bind( 'click', addTheme6 );
  $('#lt-markdown-theme7').bind( 'click', addTheme7 );
  $('#lt-markdown-theme8').bind( 'click', addTheme8 );
  $('#lt-markdown-theme9').bind( 'click', addTheme9 );


}


function addBold() {

  $("#lt-markdown-textarea").insertAtCaret("**Bold Text**");

}

function addItalic() {

  $("#lt-markdown-textarea").insertAtCaret("*Italic Text*");

}

function addOl() {

  $("#lt-markdown-textarea").insertAtCaret("1. ");

}

function addUl() {

  $("#lt-markdown-textarea").insertAtCaret("* ");

}

function addCode() {

  $("#lt-markdown-textarea").insertAtCaret("```\nYour code here...\n```");
}

function addLink() {

  $("#lt-markdown-textarea").insertAtCaret("[Link Text](Link URL)");

}

function addLine() {

  $("#lt-markdown-textarea").insertAtCaret("* * *");

}

function addQuote() {

  $("#lt-markdown-textarea").insertAtCaret("> ");

}

function addH1() {$("#lt-markdown-textarea").insertAtCaret("# Your title here... #");}
function addH2() {$("#lt-markdown-textarea").insertAtCaret("## Your title here... ##");}
function addH3() {$("#lt-markdown-textarea").insertAtCaret("### Your title here... ###");}
function addH4() {$("#lt-markdown-textarea").insertAtCaret("#### Your title here... ####");}
function addH5() {$("#lt-markdown-textarea").insertAtCaret("##### Your title here... #####");}

$(function(){
	$("#send").click(function(){
		$("#lt-markdown-secret").attr("value", "off");
	});
});

$(function(){
	$("#form-input").click(function(){
		$("#lt-markdown-secret").attr("value", "on");
	});
});

function addTheme1() {$("#lt-markdown-cur-theme").val("United");}
function addTheme2() {$("#lt-markdown-cur-theme").val("Cerulean");}
function addTheme3() {$("#lt-markdown-cur-theme").val("Cyborg");}
function addTheme4() {$("#lt-markdown-cur-theme").val("Journal");}
function addTheme5() {$("#lt-markdown-cur-theme").val("Readable");}
function addTheme6() {$("#lt-markdown-cur-theme").val("Simplex");}
function addTheme7() {$("#lt-markdown-cur-theme").val("Slate");}
function addTheme8() {$("#lt-markdown-cur-theme").val("Spacelab");}
function addTheme9() {$("#lt-markdown-cur-theme").val("Superhero");}