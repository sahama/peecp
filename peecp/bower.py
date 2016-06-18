import pyramid_bowerstatic
from pyramid.events import subscriber
from pyramid.events import NewRequest
from pyramid.events import BeforeRender
from pyramid.events import ContextFound

from .locations import base, join
import os
components = pyramid_bowerstatic.create_components('peecp', join('static', 'bower_components'))

@subscriber(BeforeRender)
def render_messages(event):
    request = event.get('request')
    _ = request.translate
    direction = _('direction')

    if direction == 'rtl':
        request.include(components, 'bootstrap-rtl')
    else:
        request.include(components, 'bootstrap')
    request.include(components, 'font-awesome')




#
# def includeme(config):
