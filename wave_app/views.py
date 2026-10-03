import json

from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse
from django.http import HttpResponseServerError, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

from .models import Wave, Bottle, WaveUser, FACILITATOR, PARTICIPANT, INPUT_TYPE, PULSE_CHECK, BOTTLE_EXCHANGE
from .forms import WaveForm, FacilitatorRegistrationForm, ParticipantRegistrationForm, BottleExchangeForm, PulseCheckForm, FacilitatorAccountForm, ParticipantAccountForm
from .constants import MY_WAVES_NAME, WAVE_NAME, WAVE_REGISTRATION, WAVE_INPUT_STATUS_API_URL
from .api import create_wave_qr_code
from .exceptions import ViewException

def home_redirect(request):
    """ This allows me to redirect facilitators to my_waves and participants to the wave they belong to """
    if request.user.is_authenticated:
        if request.user.user_type == PARTICIPANT:
            # participant_id = request.user.id
            # paticipant = Participant.objects.get(pk=participant_id)
            return redirect(WAVE_NAME, wave_id=request.user.wave_id) 
        else:
            """ Facilitators go to my_waves """
            return redirect(MY_WAVES_NAME) 
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}") 


def my_waves(request):
    """ Display the logged in facilitators's wave records """
    if request.user.is_authenticated and request.user.user_type == FACILITATOR:
        facilitator_id = request.user.id
        my_waves = Wave.objects.filter(facilitator_id=facilitator_id)
        context = {
            "facilitator_id": facilitator_id,
            "my_waves": my_waves
        }
        return render(request, "wave/my_waves.html", context)
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

 
def wave_for_participant (request, wave_id):
    if request.user.is_authenticated and request.user.user_type == PARTICIPANT:
        if request.user.wave_id == wave_id:
            error = None
            show_bottle_exchange = None
            received_bottle = None
            
            try:
                wave = Wave.objects.get(pk=wave_id)
                pulse_check_form = PulseCheckForm()
                bottle_exchange_form = BottleExchangeForm(wave_id=wave_id,sender_id=request.user.id)
                bottle = None
                if request.method == 'POST':
                    if int(request.POST['form_type']) == BOTTLE_EXCHANGE:
                        bottle_exchange_form = BottleExchangeForm(wave_id, request.user.id, request.POST)
                        if bottle_exchange_form.is_valid():
                            sender_id = request.user.id
                            sender = WaveUser.objects.get(pk=sender_id)
                            recipient_join_order = sender.join_order + 1
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
                                    raise ViewException("Alone in the wave. No other users have joined to send a bottle to.")
                                
                                recipient_join_order = recipient_join_order - all_participants.count()
                                recipient = WaveUser.objects.filter(
                                    join_order=recipient_join_order, 
                                    wave_id=wave_id,
                                    user_type=PARTICIPANT
                                )
                                if recipient.count() == 0:
                                    raise ViewException("Alone in the wave. No other users have joined to send a bottle to.")
                                
                            elif recipient.count() > 1:
                                raise ViewException("Multiple Recipients found. Could not send bottle.")
                    
                            recipient = recipient.first()
                            print('recipient', recipient)
                        
                            
                            bottle = bottle_exchange_form.save(commit=False)
                            bottle.recipient_id = recipient.id
                            bottle.wave_id = wave_id
                            bottle.sender_id = request.user.id
                            bottle.input_type = BOTTLE_EXCHANGE
                            bottle.release_number = wave.bottle_releases + 1
                            bottle.is_flagged = False
                            bottle.save()
                    else:
                        pulse_check_form = PulseCheckForm(request.POST)
                        if pulse_check_form.is_valid():
                            pulse_check = pulse_check_form.save(commit=False)
                            pulse_check.wave_id = wave_id
                            pulse_check.sender_id = request.user.id
                            pulse_check.recipient_id = wave.facilitator_id
                            pulse_check.release_number = 0
                            pulse_check.input_type = PULSE_CHECK
                            pulse_check.is_flagged = False
                            pulse_check.save()
                            print('pulse_check save. release_number:', pulse_check.release_number)
                else:
                    bottle = Bottle.objects.filter(sender_id=request.user.id, wave_id=wave_id, input_type=BOTTLE_EXCHANGE).order_by("-release_number", "pk").first()
                
                show_bottle_exchange = bottle == None or wave.bottle_releases > bottle.release_number
                received_bottle = Bottle.objects.filter(
                    wave_id=wave_id, 
                    recipient_id=request.user.id, 
                    input_type=BOTTLE_EXCHANGE, 
                    release_number=wave.bottle_releases + 1
                ).first()
            except ViewException as e:
                print('ViewException: ', e)
                error = str(e)
                show_bottle_exchange = True

            context = {
                "wave": wave,
                "INPUT_TYPE": {
                    "BOTTLE_EXCHANGE": BOTTLE_EXCHANGE,
                    "PULSE_CHECK": PULSE_CHECK,
                },
                "pulse_check_form": pulse_check_form,
                "bottle_exchange_form": bottle_exchange_form,
                "bottle": bottle,
                "show_bottle_exchange": show_bottle_exchange,
                "received_bottle": received_bottle,
                "error": error
            }
            print('context', context)
            return render(request, "wave/wave_for_participant.html", context)
        else:
            logout(request)
    return redirect(WAVE_REGISTRATION, wave_id=wave_id)


def wave_for_presentation(request, wave_id):
    """ Display wave on screen for presentation, includes QR code and submitted messages for pulse check """
    if request.user.is_authenticated and request.user.user_type == FACILITATOR:
        facilitator_id = request.user.id
        wave = Wave.objects.get(pk=wave_id)
        print('wave', wave, wave.input_type)
        if wave.facilitator_id != facilitator_id:
            return redirect(f"{settings.LOGIN_URL}")
        qr = create_wave_qr_code(request, wave_id)
        API_URL = request.scheme + '://' + request.get_host() + reverse(
            WAVE_INPUT_STATUS_API_URL,
        )
        pulse_checks = Bottle.objects.filter(wave_id=wave_id, input_type=PULSE_CHECK)
        
        """ TODO: Fix buttons so we can turn off pulse checks and bottle exchange"""
        
        
        context = {
            "facilitator_id": facilitator_id,
            "wave": wave,
            "qr": qr,
            "API_URL": API_URL,
            "pulse_checks": pulse_checks,
            "INPUT_TYPE": {
                "BOTTLE_EXCHANGE": BOTTLE_EXCHANGE,
                "PULSE_CHECK": PULSE_CHECK,
            },
        }
        return render(request, "wave/wave_for_presentation.html", context)
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
@csrf_exempt    
def wave_input_api(request):
    if request.user.is_authenticated and request.user.user_type == FACILITATOR and request.method == 'POST':
        facilitator_id = request.user.id
        data = json.loads(request.body)
        print('data', data)
        wave_id = data['wave_id']
        input_type = data['input_type']
        wave = Wave.objects.get(pk=wave_id)
        if wave.facilitator_id != facilitator_id:
            return HttpResponseServerError("Not your wave")
        wave.input_type = input_type
        wave.save()
        return HttpResponse(json.dumps({'message': 'OKAY'}), content_type='application/json')
    else:
        return HttpResponseServerError("Not a facilitator")
   

def create_wave(request):
    """ Display the 'Add New Wave' form and handle creation of a new wave """    
    if request.user.is_authenticated and request.user.user_type == FACILITATOR:
        if request.method == 'POST':
            form = WaveForm(request.POST)
    
            if form.is_valid():
                wave = form.save(commit=False)
                wave.facilitator_id = request.user.id
                wave.save()
                return redirect(MY_WAVES_NAME)
        
        else:
            form = WaveForm()
        
        return render(
            request,
            'wave/wave_form.html',
            {'form': form}
        )
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
    
def account_details(request):
    """ Display and update user's account details """    
    if request.user.is_authenticated:
        result = None
        if request.user.user_type == FACILITATOR: 
            facilitator = WaveUser.objects.get(pk=request.user.id)
            if request.method == 'POST':
                form = FacilitatorAccountForm(request.POST, instance=facilitator)
        
                if form.is_valid():
                    facilitator = form.save(commit=False)
                    facilitator.updated_date = timezone.now()
                    facilitator.save()
                    result = 'Facilitor account updated'
            
            else:
                form = FacilitatorAccountForm(instance=facilitator)
            
        else: 
            participant = WaveUser.objects.get(pk=request.user.id)
            if request.method == 'POST':
                form = ParticipantAccountForm(request.POST, instance=participant)
        
                if form.is_valid():
                    participant = form.save(commit=False)
                    participant.updated_date = timezone.now()
                    participant.save()
                    result = 'Participant account updated'
            
            else:
                form = ParticipantAccountForm(instance=participant)
        
        return render(
            request,
            'account_details.html',
            {'form': form, 'result': result}
        )
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")


def facilitator_registration(request):
    """ Display the registration form and create a new facilitator account """
    if request.user.is_authenticated == False:
        result = None
        if request.method == 'POST':
            form = FacilitatorRegistrationForm(request.POST)
  
            if form.is_valid():
                facilitator = form.save(commit=False)
                facilitator.join_order = 0
                facilitator.save()
             
                """ automatically login after registering """
                new_user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                )
                login(request, new_user)
                return redirect(MY_WAVES_NAME)
       
        else:
            form = FacilitatorRegistrationForm()
     
        return render(
            request,
            'registration.html',
            {'form': form, 'result': result, 'user_type': 'Facilitator'}
        )
    else:
        return redirect('')

 
def participant_registration(request, wave_id):
    """ Display the registration form and create a new participant account """
    if request.user.is_authenticated == False and wave_id != None:
        result = None
        if request.method == 'POST':
            form = ParticipantRegistrationForm(wave_id, request.POST)
            form.wave_id = wave_id
        
    
            form.requested_follow_up = False
            form.user_type = PARTICIPANT
            form.is_staff = False
            form.is_superuser = False

            if form.is_valid():
                participant = form.save(commit=False)

                """ Get the join_order from the latest participant to join and add 1 """
                last_participant = WaveUser.objects.filter(wave_id=wave_id, user_type=PARTICIPANT).aggregate(Max('join_order'))
                print('last_participant', last_participant, last_participant["join_order__max"], last_participant["join_order__max"] == 0)
                
                if last_participant["join_order__max"] == None or last_participant["join_order__max"] == 0:
                    join_order = 1
                else:
                    join_order = last_participant["join_order__max"] + 1

                participant.join_order = join_order
                participant.save()

                """ automatically login after registering """
                new_user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                )
                login(request, new_user)
                return redirect(WAVE_NAME, wave_id=wave_id)

        else:
            form = ParticipantRegistrationForm(wave_id=wave_id)

        return render(
            request,
            'registration.html',
            {
                'form': form, 
                'result': result, 
                'user_type': 'Participant'
            }
        )
    else:
        return redirect('/')
    

def resources (request):
    return render(
        request,
        'resources.html',
    )