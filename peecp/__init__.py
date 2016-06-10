from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import SessionAuthenticationPolicy
from .security import group_finder, RootFactory
from .i18n import custom_locale_negotiator

authn_policy = SessionAuthenticationPolicy(callback=group_finder)
authz_policy = ACLAuthorizationPolicy()



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=RootFactory)

    #TODO: do some thing to generate secret string in new installation
    session_factory = SignedCookieSessionFactory(secret='h@k%^jh%j',timeout=3600, max_age=3600)
    config.set_session_factory(session_factory)

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_translation_dirs('peecp:locale')

    config.set_locale_negotiator(custom_locale_negotiator)


    config.include('pyramid_jinja2')
    config.include('pyramid_bowerstatic')
    config.include('.models')
    config.include('.routes')
    config.scan()
    config.scan('.i18n')

    return config.make_wsgi_app()
