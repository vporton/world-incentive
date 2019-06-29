from django.forms import widgets


class VoteWidget(widgets.Widget):
    template_name = 'initiative/widgets/votewidget.html'

    class Media:
        js = ('js/vote.js',)

    def __init__(self, vote_for_text, vote_against_text, *kwargs):
        super().__init__(*kwargs)
        self.vote_for_text = vote_for_text
        self.vote_against_text = vote_against_text

    def format_value(self, value):
        return value

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['vote_for_text'] = self.vote_for_text
        context['vote_against_text'] = self.vote_against_text
        return context
