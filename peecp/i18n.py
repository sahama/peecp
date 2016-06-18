from pyramid.i18n import get_localizer, TranslationStringFactory

from pyramid.events import subscriber
from pyramid.events import NewRequest
from pyramid.events import BeforeRender

from webob.acceptparse import Accept

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_request
from pyramid.request import Request


tsf = TranslationStringFactory('peecp')

LOCALES = ('fa', 'en')

# NOTICE: we use it in later to get lang from database
def custom_locale_negotiator(request):
    """ The :term:`custom locale negotiator`. Returns a locale name.

    - First, the negotiator looks for the ``_LOCALE_`` attribute of
      the request object (possibly set by a view or a listener for an
      :term:`event`).

    - Then it looks for the ``request.params['_LOCALE_']`` value.

    - Then it looks for the ``request.cookies['_LOCALE_']`` value.

    - Then it looks for the ``Accept-Language`` header value,
      which is set by the user in his/her browser configuration.

    - Finally, if the locale could not be determined via any of
      the previous checks, the negotiator returns the
      :term:`default locale name`.
    """

    name = '_LOCALE_'
    locale_name = getattr(request, name, None)
    if locale_name is None:
        locale_name = request.params.get(name)
        if locale_name is None:
            locale_name = request.cookies.get(name)
            if locale_name is None:
                locale_name = request.accept_language.best_match(
                    LOCALES, request.registry.settings.default_locale_name)
                if not request.accept_language:
                    # If browser has no language configuration
                    # the default locale name is returned.
                    locale_name = request.registry.settings.default_locale_name
    return locale_name


@subscriber(BeforeRender)
def add_renderer_globals(event):
    request = event.get('request')
    if request is None:
        request = get_current_request()
    event['_'] = request.translate

    event['print'] = print

    event['localizer'] = request.localizer


@subscriber(NewRequest)
def add_localizer(event):
    request = event.request
    localizer = get_localizer(request)

    if '_LOCALE_' in request.GET:
        language = request.GET['_LOCALE_']
        print('lang is ', language)
        response = request.response
        response.set_cookie('_LOCALE_',
                            value=language,
                            max_age=31536000)


    def auto_translate(string, mapping=None, domain=None):
        return localizer.translate(tsf(string),mapping=mapping, domain=domain)
    request.localizer = localizer
    request.translate = auto_translate




# @view_config(route_name='locale')
def set_locale_cookie(request):
    if 'language' in request.GET:
        language = request.GET['language']
        response = Response()
        response.set_cookie('_LOCALE_',
                            value=language,
                            max_age=31536000)  # max_age = year
    return HTTPFound(location='/',
                     headers=response.headers)


# class MyRequest(Request):
#     pass


def includeme(config):
    config.add_translation_dirs('peecp:locale')
    config.set_locale_negotiator(custom_locale_negotiator)
    # config.set_request_factory(MyRequest)
    # config.add_route('locale', '/locale')
