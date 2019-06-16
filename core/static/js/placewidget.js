// TODO: No fixed ID.
function update_places_list(level, from_initial=false) {
    level = Number(level);
    const val = $('#id_place_' + (level - 1)).val();
    if(val == '')
        for(var cur = level; cur < 5; ++cur)
            $('#id_place_'+cur).html("<option value=''>-</option>");
    else
        $.get('/core/cities-ajax/' + level + '/' + val, function (data) {
            $('#id_place_'+level).html("<option value=''>-</option>\n" + data);
            if(from_initial) $('#id_place_'+level).val($('#id_place_'+level+'_initial').val());
            if(level < 4)
                update_places_list(level + 1);
        });
}
