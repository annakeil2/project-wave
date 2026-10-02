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
    """A session the facilitator creates"""
    
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
    """ TODO: Allow multiple input types """
    input_type = models.IntegerField(
        choices=INPUT_TYPE.items(),
        default=0
    )
    deleted_date = models.DateTimeField(null=True, blank=True)
    moderation_type = models.IntegerField(
        choices=MODERATION_TYPE.items(),
        default=0
    )
    
    """ Keeps track of how many bottle releases the facilitator has completed """
    bottle_releases = models.IntegerField(default=0)


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
    release_number = models.IntegerField(default=None)

    

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


class WaveUserManager(BaseUserManager):
    """ Methods for creating superusers """
    
    def create_superuser(self, email, password, **kwargs):
        """Create and save a superuser with administrator privileges."""
        user = self.model(
            email=self.normalize_email(email),
            user_type=FACILITATOR, 
            is_staff=True, 
            is_superuser=True,
            **kwargs
        )
        user.set_password(password) 
        user.save(using=self._db)
        return user
    
    def create_user(self, user_type, email, password=None):
        """ Create a non-super user """
        if not email:
            raise ValueError("You must enter an email address")

        user = self.model(
            email=self.normalize_email(email),
            user_type=user_type, 
            is_staff=False,
            is_superuser=False,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class WaveUser(AbstractUser):
    """ A user inherited from both facilitator and participant """

    id = models.AutoField(primary_key=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    user_type = models.IntegerField(
        choices=USER_TYPE.items(),
    )
    
    """ Participant only properties """
    wave_id = models.IntegerField(null=True, blank=True)
    requested_follow_up = models.BooleanField(default=False)
    """ This will store an incrementing number per wave for the participant
    that we can use for the pseudo-randomisation of bottle messages """
    join_order = models.IntegerField(default=1)
    
    objects = WaveUserManager()

    def __str__(self):
        return f"WaveUser({self.id}, {self.username})"
    

Participant = WaveUser

Facilitator = WaveUser


# class FacilitatorManager(BaseUserManager):
#     """ Methods for creating facilitators """
    
#     def create_user(self, email, password=None):
#         """ Create a non-super user """
#         if not email:
#             raise ValueError("You must enter an email address")

#         user = self.model(
#             email=self.normalize_email(email),
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user


# class Facilitator(WaveUser):
#     """ A facilitator is a user of the app who can create waves """
        
#     id = models.AutoField(primary_key=True)
#     updated_date = models.DateTimeField(null=True, blank=True)
#     user_type = models.IntegerField(
#         choices=USER_TYPE.items(),
#     )
    
#     objects = FacilitatorManager()
    
#     def save(self , *args , **kwargs):
#         self.user_type = FACILITATOR
#         return super().save(*args , **kwargs)
        
#     def __str__(self):
#         return f"Facilitator({self.id}, {self.username})"



# class ParticipantManager(BaseUserManager):
#     """ Methods for creating wave participants """
    
#     def create_user(self, email=None, password=None):        
#         """ Create a non-super user """
#         if not email:
#             user = self.model(
#                 email=None
#             )
#         else: 
#             user = self.model(
#                 email=self.normalize_email(email),
#             )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user


# class Participant(WaveUser):
#     """ A participant is a user who belongs to a specific wave """     
       
#     id = models.AutoField(primary_key=True)
#     updated_date = models.DateTimeField(null=True, blank=True)
#     user_type = models.IntegerField(
#         choices=USER_TYPE.items(),
#     )
#     wave_id = models.IntegerField()
#     # wave = models.ForeignKey(
#     #     'Wave',
#     #     on_delete=models.CASCADE,
#     #     related_name='participants'
#     # )
#     requested_follow_up = models.BooleanField(default=False)
#     """ This will store an incrementing number per wave for the participant
#     that we can use for the pseudo-randomisation of bottle messages """
#     join_order = models.IntegerField(default=1)
#     objects = ParticipantManager()

    
#     def __init__(self, *args, **kwargs):
#         self.user_type = PARTICIPANT
#         # super().__init_(*args, **kwargs)
    
#     def __str__(self):
#         id = 'None'
#         username = self.username or 'None'
#         return f"Participant({id}, {username})"





