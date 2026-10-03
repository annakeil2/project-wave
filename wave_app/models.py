from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


""" The type of bottle allowed in a wave """
BOTTLE_EXCHANGE = 1
PULSE_CHECK = 2   
INPUT_TYPE = {
    0: 'n/a',
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
    
    def create_user(self, username, user_type, email, password=None):
        """ Create a non-super user """
        if not email:
            raise ValueError("You must enter an email address")

        user = self.model(
            username=username,
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
