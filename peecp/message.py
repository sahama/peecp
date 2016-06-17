from pyramid.events import subscriber
from pyramid.events import NewRequest
from pyramid.events import BeforeRender
from pyramid.events import ContextFound


class Message:
    danger = 'danger'
    warning = 'warning'
    info = 'info'
    success = 'success'
    default = 'default'

    def __init__(self, body='', message_type=info, source='', user=None, request=None, mapping=None):
        self.type = message_type
        self.body = body
        self.source = source
        self.request = request
        self.mapping = mapping
        if user:
            self.user = user
        elif request:
            if request.authenticated_userid:
                self.user = self.request.authenticated_userid
            else:
                self.user = 'Guest'
        else:
            self.user = 'Guest'

        if not (source or body):
            self.body = 'no notice found'

    def add(self, body, message_type=None, source=None, user=None, request=None, mapping=None):
        if message_type:
            self.type = message_type
        if source:
            self.source = source
        if user:
            self.user = user
        if request:
            self.request = request
        if mapping:
            self.mapping = mapping
        self.body = body

        self.request.session.flash(
            {"type": self.type,
             'source': self.source,
             'user': self.user,
             'body': self.body,
             'mapping': self.mapping}
        )


class Safe(str):
    # get from pyramid_layput
    # Wrapping a string in this class avoids having to prefix the value
    # with `structure` in TAL

    def __html__(self):
        return self


@subscriber(NewRequest)
def add_message(event):
    request = event.request
    message = Message(request=request)
    request.message = message


@subscriber(ContextFound)
def add_message_context(event):
    request = event.request
    request.context.message = request.message


@subscriber(BeforeRender)
def render_messages(event):
    request = event.get('request')
    messages = request.session.pop_flash()
    event['messages'] = request.session.pop_flash()

    def bootstrap_renderer():
        _ = request.translate
        message_template = """<div class="alert alert-small alert-{type}" role="alert">
<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span
aria-hidden="true">&times;</span></button>
<b style="font-size: larger">{source}</b> {body}
</div>"""
        body = ''
        for message in messages:
            body += message_template.format(
                type=message['type'],
                source=_(message['source']) if message['source'] else '',
                body=_(message['body'], mapping=message['mapping'])
            )
        return Safe(body)

    event['flash_messages'] = bootstrap_renderer()


def includeme(config):
    # TODO: an action to required transtation
    pass
