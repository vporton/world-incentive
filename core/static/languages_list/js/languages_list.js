$(function() {
    // Requires jQuery UI
    $('.urls_editor ul').sortable({
        //handle: ".handle"
    });
})

function languages_list_add(widget_name, language) {
    var dummy = $('#id_'+widget_name+'_dummy')[0];
    var elt = $(dummy).clone();
//    elt.css.display = 'block';
    elt.removeAttr('style')
    elt.find('input').prop('required', true);
    elt.find('input[name=language]').val(language);
    $(dummy).parent().append(elt)
}