from django import template
from wave_app.models import Wave

register = template.Library()

@register.filter    
def display_moderation_type(type):
    """ Display moderation type of a wave """
    return Wave.MODERATION_TYPE[type]