from django.forms import widgets


class VoteWidget(widgets.Widget):
    template_name = 'initiative/widgets/votewidget.html'

    def __init__(self, vote_for_text, vote_against_text, *kwargs):
        super().__init__(*kwargs)
        self.vote_for_text = vote_for_text
        self.vote_against_text = vote_against_text

    def format_value(self, value):
        return value

    # def get_context(self, name, value, attrs):
    #     d = super().get_context(name, value, attrs)
    #     d2 = d.copy() if d is not None else {}
    #     d2['votes_for'] = self.votes_for
    #     d2['votes_against'] = self.votes_against
    #     return d2
