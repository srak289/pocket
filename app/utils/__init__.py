from mako.template import Template
from mako.lookup import TemplateLookup

from ..paths import *

mylookup = TemplateLookup([TEMPLATE_DIR])

def render_template(template, **kwargs):
    return mylookup.get_template(template).render(**kwargs)
