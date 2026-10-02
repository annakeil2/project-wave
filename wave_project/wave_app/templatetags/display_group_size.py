from django import template
from wave_app.models import Wave, Participant

register = template.Library()

@register.filter    
def display_group_size(wave):
    """ Get the group size, i.e. the number of participants of a wave """
    participants = Participant.objects.filter(wave_id=wave.id)
    
    # participants = wave.participants.all()
   
    return len(participants)
