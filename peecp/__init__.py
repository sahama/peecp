from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import SessionAuthenticationPolicy
from .security import group_finder
authn_policy = SessionAuthenticationPolicy(callback=group_finder)
authz_policy = ACLAuthorizationPolicy()

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    #TODO: do some thing to generate secret string in new installation
    session_factory = SignedCookieSessionFactory(secret='h@k%^jh%j',timeout=3600, max_age=3600)
    config.set_session_factory(session_factory)

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
