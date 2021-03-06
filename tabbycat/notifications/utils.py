from django.conf import settings
from django.core import mail

from .models import MessageSentRecord


class TournamentEmailMessage(mail.EmailMessage):
    def __init__(self, subject='', body='', tournament=None, round=None, event=None, person=None,
                 connection=None, headers={}, cc=None, bcc=None, attachments=None):

        self.person = person
        self.emails = [self.person.email]

        self.tournament = tournament
        self.round = round

        self.event = event

        self.reply_to = "%s <%s>" % (self.tournament.pref('reply_to_name'), self.tournament.pref('reply_to_address'))
        self.from_email = "%s <%s>" % (self.tournament.short_name, settings.DEFAULT_FROM_EMAIL)

        self.headers = headers
        headers['List-Unsubscribe'] = "<mailto:%s?subject=unsubscribe>" % (self.tournament.pref('reply_to_address'))
        super().__init__(subject, body, self.from_email, self.emails, bcc, connection, attachments,
            self.headers, cc, [self.reply_to])

    def as_model(self):
        return MessageSentRecord(recepient=self.person, event=self.event, method=MessageSentRecord.METHOD_TYPE_EMAIL, round=self.round, tournament=self.tournament)
