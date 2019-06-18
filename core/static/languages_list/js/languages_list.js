$(function() {
    // Requires jQuery UI
    $('.languages_list ul').sortable({
        handle: ".handle"
    });
})

function languages_list_add(widget_name, language) {
    var dummy = $('#id_'+widget_name+'_dummy')[0];
    var elt = $(dummy).clone();
//    elt.css.display = 'block';
    elt.removeAttr('style')
    elt.find('[name=language]').val(language);
    $(dummy).parent().append(elt)
}