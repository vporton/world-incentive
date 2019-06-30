function ajax_vote(pool, reclaim, pk, against, name) {
    $.post(
        '/initiative/ajax-vote/' +
            pool + ':' + (against ? 1 : 0) + ':' + (reclaim ? 1 : 0) + '/' + pk,
        function () {
            $('#' + name + (against ? '_against' : '_for') + (reclaim ? '_reclaim_btn_id' : '_vote_btn_id')).css('display', 'none');
            $('#' + name + (against ? '_against' : '_for') + (reclaim ? '_vote_btn_id' : '_reclaim_btn_id')).css('display', 'inline');

            $('#' + name + (against ? '_for' : '_against') + '_reclaim_btn_id').css('display', 'none');
            $('#' + name + (against ? '_for' : '_against') + '_vote_btn_id').css('display', 'inline');
        });
    return false;
}