from django import template
from wave_app.models import INPUT_TYPE

register = template.Library()

@register.filter    
def display_input_type(type):
    """ Display input type (i.e. pulsecheck or bottle exchange) of a wave """
    return INPUT_TYPE[type]