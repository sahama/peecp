import pyramid_bowerstatic
from .locations import base, join
import os
components = pyramid_bowerstatic.create_components('peecp', join('static', 'bower_components'))