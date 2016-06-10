from pyramid.response import Response
from pyramid.view import view_config
from pyramid.request import Request as request
from ..bower import components

from sqlalchemy.exc import DBAPIError

from ..models import MyModel
from pyramid.i18n import TranslationString

@view_config(route_name='home', renderer='../templates/default.jinja2')
def my_view(request=request): # request=requesr is just for autocomplete
    # ts = TranslationString('direction', domain='peecp')
    # localizer = request.localizer
    # translated = localizer.translate(ts)
    # print(ts, localizer, translated)
    _ = request.translate
    direction = _('direction')

    if direction == 'rtl':
        request.include(components, 'bootstrap-rtl')
    else:
        request.include(components, 'bootstrap')
    user = request.authenticated_userid
    return {'user': user}
