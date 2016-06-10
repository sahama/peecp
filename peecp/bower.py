import pyramid_bowerstatic
from .locations import base, join
import os
components = pyramid_bowerstatic.create_components('jquery', join('static', 'bower_components'))