import syslog
import time

class Message():
    danger = 'danger'
    warning = 'warning'
    info = 'info'
    success = 'success'
    default = 'default'

    def __init__(self, body='', message_type=info, source='', user=None, request=None, mapping={}):
        self.type = message_type
        self.body = body
        self.source = source
        self.request = request
        self.mapping = {}
        if user:
            self.user = user
        elif request:
            if request.authenticated_userid:
                self.user = self.request.authenticated_userid
        else:
            self.user = 'Guest'

        if not (source or body):
            self.body = 'no notice found'
            self.type = Message.info

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

        self.request.session.flash({"type": self.type, 'source': self.source, 'user': self.user, 'body': self.body, 'mapping': self.mapping})

    def __repr__(self):

        # return 'source:{0} ip:{4} type:{1} user:{2} message:{3}'.format(
        return '{0} {1} {2} {3} {4} {5}'.format(
            self.source,
            self.type,
            self.user,
            self.body,
            self.translated_mapping,
            (lambda x : x.remote_addr if x else '')(self.request)
        )

    def __str__(self):
        return self.__repr__()




