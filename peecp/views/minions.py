from pyramid.response import Response
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.request import Request as request
from ..bower import components
from ..models.salt import SaltApi

from sqlalchemy.exc import DBAPIError

from ..models import MyModel
from pyramid.i18n import TranslationString

@view_defaults(route_name='minions', renderer='../templates/minions.jinja2')
class MinionsView():
    def __init__(self, context, request=request):
        self.request = request
        self.context = context
        user = request.authenticated_userid
        self.context.message.add('hello',source='main')

        print(self.request.session)
        self.salt = SaltApi(self.request.session['salt']['token'])
    @view_config()
    def main(self):
        minions = self.salt.run('test.ping')
        print(minions)
        return {'minions': minions}
