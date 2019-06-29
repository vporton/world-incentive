from django.forms import widgets


class VoteWidget(widgets.Widget):
    template_name = 'initiative/widgets/votewidget.html'

    def __init__(self, vote_for_text, vote_against_text, *kwargs):
        super().__init__(*kwargs)
        self.vote_for_text = vote_for_text
        self.vote_against_text = vote_against_text