from pyramid.response import Response
from pyramid.view import view_config
from pyramid.request import Request as request
from ..bower import components

from sqlalchemy.exc import DBAPIError

from ..models import MyModel


@view_config(route_name='home', renderer='../templates/default.jinja2')
def my_view(request=request): # request=requesr is just for autocomplete
    user = request.authenticated_userid
    request.include(components, 'jquery')
    return {'user': user}
