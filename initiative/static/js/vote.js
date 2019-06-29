function ajax_vote(pool, reclaim, initiative_pk, ours, other, against) {
    $.post(
        '/initiative/ajax-vote/' +
            pool + ':' + (against ? 1 : 0) + ':' + (reclaim ? 1 : 0) + '/' + initiative_pk,
        function () {
            $('#'+ours).css('display', 'none');
            $('#'+other).css('display', 'inline');
        });
    return false;
}