from django import template
from wave_app.models import Wave

register = template.Library()

@register.filter    
def display_group_size(wave):
    """ Get the group size, i.e. the number of participants of a wave """
    participants = wave.participant_set.all()
   
    return len(participants)
