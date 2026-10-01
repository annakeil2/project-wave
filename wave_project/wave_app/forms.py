from django import forms
from .models import Wave, Bottle, Announcement, Facilitator, Participant

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
    def __init__(self, form_type, *args, **kwargs):
        super(PulseCheckForm, self).__init__(*args, **kwargs)
        self.fields['form_type'].initial = form_type
    class Meta:
        model = Bottle

        fields = [
            'message',
        ]


class BottleExchangeForm(forms.ModelForm):
    """ A form for participants to submit their bottled messages """
    form_type = forms.IntegerField(widget=forms.HiddenInput())
    def __init__(self, form_type, *args, **kwargs):
        super(BottleExchangeForm, self).__init__(*args, **kwargs)
        self.fields['form_type'].initial = form_type
    class Meta:
        model = Bottle

        fields = [
            'message',
        ]

# class MessageForm(forms.ModelForm):
#     """A form for creating messages"""
#     def __init__(self, *args, **kwargs):
#         """Initialise the form and exclude the sender from the recipient list."""
#         sender_id = kwargs.pop('sender_id')
#         super(MessageForm, self).__init__(*args, **kwargs)
#         raw_staff = Employee.objects.exclude(id=sender_id)
#         staff = [(q.id, q.get_full_name()) for q in raw_staff]
#         self.fields['receiver_user_id'] = forms.ChoiceField(
#             choices=tuple(staff)
#         )

 
#     class Meta:
#         model = Message

#         fields = [
#             'id',
#             # 'sender_user_id',
#             'receiver_user_id',
#             'subject',
#             'body',
#             # 'message_status',
#         ]

#         widgets = {
#             'body': forms.Textarea(
#                 attrs={'cols': 80, 'rows': 20}
#             ),
#         }
       
        
# class EmployeeForm(forms.ModelForm):
#     """A form for viewing and updating employee details."""
#     def __init__(self, *args, **kwargs):
#         """Initialise the form and exclude the sender from the recipient list."""
#         super(EmployeeForm, self).__init__(*args, **kwargs)
#         self.fields['email'].required = True
    
        
#     class Meta:
#         model = Employee

#         fields = [
#             'username',
#             'first_name',
#             'last_name',
#             'email'
#         ]


class FacilitatorRegistrationForm(forms.ModelForm):
    """ A form for registering a new facilitator account """
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        """Initialise the form and make the email field required."""
        super(FacilitatorRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
    
       
    class Meta:
        model = Facilitator

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
    
       
    class Meta:
        model = Participant

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
        if commit: 
            user.save()
        return user