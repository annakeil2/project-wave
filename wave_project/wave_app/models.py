from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


""" The type of bottle allowed in a wave """
BOTTLE_EXCHANGE = 1
PULSE_CHECK = 2   
INPUT_TYPE = {
    BOTTLE_EXCHANGE: "Bottle exchange",
    PULSE_CHECK: "Pulse check",
}

FACILITATOR = 1
PARTICIPANT = 2   
USER_TYPE = {
    FACILITATOR: "Facilitator",
    PARTICIPANT: "Participant",
}

    
class Wave(models.Model):
    """"A session the facilitator creates"""
    
    AI_MODERATION = 1  
    MODERATION_TYPE = {
        AI_MODERATION: "AI moderation",
    }
    
    id = models.AutoField(primary_key=True)
    wave_name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    facilitator_id = models.IntegerField()
    event_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    input_type = models.IntegerField(
        """" TODO: Allow multiple input types """
        choices=INPUT_TYPE.items(),
        default=0
    )
    deleted_date = models.DateTimeField(null=True, blank=True)
    moderation_type = models.IntegerField(
        choices=INPUT_TYPE.items(),
        default=0
    )
    

class Bottle (models.Model):
    
    id = models.AutoField(primary_key=True)
    wave_id = models.IntegerField()
    sender_id = models.IntegerField()
    recipient_id = models.IntegerField()
    message = models.CharField(max_length=1500000)
    input_type = models.IntegerField(
        choices=INPUT_TYPE.items(),
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_flagged = models.BooleanField()

    

class Announcement(models.Model):
    id = models.AutoField(primary_key=True)  
    wave_id = models.IntegerField()
    sender_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    prompt = models.CharField(max_length=1500000)
    request_input_type = models.IntegerField(
        choices=INPUT_TYPE.items(),
        default=0
    )


class WaveUser(AbstractUser):
    """ A user inherited from both facilitator and participant """

    id = models.AutoField(primary_key=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    user_type = models.IntegerField(
        choices=USER_TYPE.items(),
    )

    def __str__(self):
        return f"WaveUser({self.id}, {self.username})"


class FacilitatorManager(BaseUserManager):
    """ Methods for creating facilitators """
    
    def create_user(self, email, password=None):
        """ Create a non-super user """
        if not email:
            raise ValueError("You must enter an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class Facilitator(WaveUser):
    """ A facilitator is a user of the app who can create waves """
    class Meta :
        proxy = True
    objects = FacilitatorManager()
    
    def save(self , *args , **kwargs):
        self.user_type = FACILITATOR
        return super().save(*args , **kwargs)
        
    def __str__(self):
        return f"Facilitator({self.id}, {self.username})"



class ParticipantManager(BaseUserManager):
    """ Methods for creating wave participants """
    
    def create_user(self, email=None, password=None):
        """ Create a non-super user """
        if not email:
            user = self.model(
                email=None
           )
        else: 
            user = self.model(
                email=self.normalize_email(email),
            )

        user.set_password(password)
        user.save(using=self._db)
        return user


class Participant(WaveUser):
    """ A participant is a user who belongs to a specific wave """
    wave_id = models.IntegerField()
    requested_follow_up = models.BooleanField()
    
    def __init__(self):
        self.user_type = PARTICIPANT
    
    def __str__(self):
        return f"Participant({self.id}, {self.username})"





