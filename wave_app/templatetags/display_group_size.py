from django import template
from wave_app.models import Wave, WaveUser, PARTICIPANT

register = template.Library()

@register.filter    
def display_group_size(wave):
    """ Get the group size, i.e. the number of participants of a wave """
    participants = WaveUser.objects.filter(wave_id=wave.id, user_type=PARTICIPANT)
   
    return len(participants)
