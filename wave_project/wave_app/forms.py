from django import forms
from .models import Wave, Bottle, Announcement, WaveUser, BOTTLE_EXCHANGE, PULSE_CHECK, PARTICIPANT, FACILITATOR

class WaveForm(forms.ModelForm):
    """ A form for creating and updating waves """
    class Meta:
        model = Wave

        fields = [
            'wave_name',
            'event_date',
            'input_type',
            'moderation_type',
        ]

        widgets = {
            'event_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
        }


class PulseCheckForm(forms.ModelForm):
    """ A form for participants to submit their bottled messages """
    form_type = forms.IntegerField(widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        super(PulseCheckForm, self).__init__(*args, **kwargs)
        self.fields['form_type'].initial = PULSE_CHECK
    class Meta:
        model = Bottle

        fields = [
            'message',
        ]


class BottleExchangeForm(forms.ModelForm):
    """ A form for participants to submit their bottled messages """
    form_type = forms.IntegerField(widget=forms.HiddenInput())
    
    
    def __init__(self, wave_id, sender_id, *args, **kwargs):
        """ Initialise the form and exclude the sender from the recipient list """
        wave = Wave.objects.get(pk=wave_id)
        sender = WaveUser.objects.get(pk=sender_id)
        recipient_join_order = sender.join_order + wave.bottle_releases + 1
        print('recipient_join_order', recipient_join_order)
        all_participants = WaveUser.objects.filter(
            wave_id=wave_id,
            user_type=PARTICIPANT
        )
        recipient = WaveUser.objects.filter(
            join_order=recipient_join_order, 
            wave_id=wave_id,
            user_type=PARTICIPANT
        )
        if recipient.count() == 0:
            if all_participants.count() < 2:
                raise "Recipient not found"
            
            recipient_join_order = recipient_join_order - all_participants.count()
            recipient = WaveUser.objects.filter(
                join_order=recipient_join_order, 
                wave_id=wave_id,
                user_type=PARTICIPANT
            )
            if recipient.count() == 0:
                raise "Recipient not found"
            
        elif recipient.count() > 1:
            raise "Multiple Recipients found"

        recipient = recipient.first()
        print('recipient', recipient)

        super(BottleExchangeForm, self).__init__(*args, **kwargs)
        self.fields['recipient_id'].initial = recipient.id
        self.fields['form_type'].initial = BOTTLE_EXCHANGE
    class Meta:
        model = Bottle

        fields = [
            'message',
            'recipient_id'
        ]
        
        widgets = {
            'recipient_id': forms.HiddenInput(),
        }


class FacilitatorRegistrationForm(forms.ModelForm):
    """ A form for registering a new facilitator account """
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        """Initialise the form and make the email field required."""
        super(FacilitatorRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.user_type = FACILITATOR
    
       
    class Meta:
        model = WaveUser

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]
    
    
    def save(self, commit=True):
        """Create the facilitator and securely hash their password."""
        user = super().save(commit=False)
        user.user_type = FACILITATOR
        user.set_password(self.cleaned_data["password"])
        if commit: 
            user.save()
        return user
    
    
class ParticipantRegistrationForm(forms.ModelForm):
    """ A form for registering a new participant account """
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    wave_id = forms.IntegerField(widget=forms.HiddenInput())
    
    def __init__(self, wave_id, *args, **kwargs):
        """ Initialise the form and make the email field optional """
        super(ParticipantRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['wave_id'].initial = wave_id
        self.user_type = PARTICIPANT
       
    class Meta:
        model = WaveUser

        fields = [
            'wave_id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]
    
    
    def save(self, commit=True):
        """Create the facilitator and securely hash their password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.user_type = PARTICIPANT
        # user.wave = Wave.objects.get(pk=self.wave_id)
        if commit: 
            user.save()
        return user
    

class FacilitatorAccountForm(forms.ModelForm):
    """ A form for editing facilitator account details """
    def __init__(self, *args, **kwargs):
            """Initialise the form and make the email field required."""
            super(FacilitatorAccountForm, self).__init__(*args, **kwargs)
            self.fields['email'].required = True
            
    class Meta:
        model = WaveUser
    
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
        
class ParticipantAccountForm(forms.ModelForm):
    """ A form for editing participant account details """
    class Meta:
        model = WaveUser
    
        fields = [
            'first_name',
            'last_name',
            'email',
        ]