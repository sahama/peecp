from pyramid.response import Response
from pyramid.view import view_config
from pyramid.request import Request as request
from ..bower import components

from sqlalchemy.exc import DBAPIError

from ..models import MyModel
from pyramid.i18n import TranslationString

@view_config(route_name='home', renderer='../templates/default.jinja2')
def my_view(context, request=request): # request=requesr is just for autocomplete
    user = request.authenticated_userid
    context.message.add('hello',source='main')
    # print(request.session)
    return {'user': user}
