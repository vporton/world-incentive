$(document).ajaxError(function( event, request, settings ) {
    alert("Error: " + request.status); // TODO: Localize.
});

//This function gets cookie with a given name
function getCookie(name) {
 var cookieValue = null;
 if (document.cookie && document.cookie != '') {
     var cookies = document.cookie.split(';');
     for (var i = 0; i < cookies.length; i++) {
         var cookie = jQuery.trim(cookies[i]);
         // Does this cookie string begin with the name we want?
         if (cookie.substring(0, name.length + 1) == (name + '=')) {
             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
         break;
     }
 }
 }
 return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
 // these HTTP methods do not require CSRF protection
 return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
 beforeSend: function(xhr, settings) {
     if (!csrfSafeMethod(settings.type) && !this.crossDomain &&
        (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)))) {
     // Only send the token to relative URLs i.e. locally.
     xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
     }
 }
});

(function($){
    $(document).ready(function(){
        $('ul.dropdown-menu [data-toggle=dropdown]').on('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            $(this).parent().siblings().removeClass('open');
            $(this).parent().toggleClass('open');
        });
    });
})(jQuery);

function set_language(lang) {
    $.post('/core/set-language', {lang: lang}, function() {
        location.reload();
    });
}

function ajax_dialog(url, arg) {
    $('#dialog').remove();
    $('body').addClass('wait')
    $.get(url, function(html) {
        $('body').append(html);
        $('#dialog').dialog(arg);
        $('body').removeClass('wait')
    });
    return false;
}

function ajax_create_initiative_prompt(url) {
    return ajax_dialog(url, {
        buttons: [
            {
                text: "OK",
                click: function () {
                    $(this).dialog("close");
                    $('form', this).submit();
                }
            },
            {
                text: "Cancel",
                click: function () {
                    $(this).dialog("close");
                }
            }
        ],
        width: 600
    });
}