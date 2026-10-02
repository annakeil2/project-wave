from django.shortcuts import render, redirect

from .models import Wave, Bottle, Announcement, Facilitator, Participant, FACILITATOR, PARTICIPANT, INPUT_TYPE
from django.conf import settings
from .forms import WaveForm, FacilitatorRegistrationForm, ParticipantRegistrationForm, BottleExchangeForm, PulseCheckForm
# from . import services
from django.utils import timezone
from .constants import MY_WAVES_NAME, WAVE_NAME, WAVE_REGISTRATION
from .API import create_wave_QR_code
from django.contrib.auth import logout, authenticate, login


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
            wave = Wave.objects.get(pk=wave_id)
            pulse_check_form = PulseCheckForm()
            bottle_exchange_form = BottleExchangeForm(wave_id=wave_id,sender_id=request.user.id)
            if request.method == 'POST':
                if request.POST.form_type == INPUT_TYPE.BOTTLE_EXCHANGE:
                    bottle_exchange_form = BottleExchangeForm(wave_id, request.user.id, request.POST)
                    if bottle_exchange_form.is_valid():
                        bottle = bottle_exchange_form.save(commit=False)
                        bottle.wave_id = wave_id
                        bottle.sender_id = request.user.id
                        bottle.input_type = INPUT_TYPE.BOTTLE_EXCHANGE
                        bottle.release_number = wave.bottle_releases + 1
                        bottle.save()
                else:
                    pulse_check_form = PulseCheckForm(request.POST)
                    if pulse_check_form.is_valid():
                        bottle = pulse_check_form.save(commit=False)
                        bottle.wave_id = wave_id
                        bottle.sender_id = request.user.id
                        bottle.recipient_id = wave.facilitator_id
                        bottle.input_type = INPUT_TYPE.PULSE_CHECK
                        bottle.save()
            context = {
                "wave": wave,
                "INPUT_TYPE": INPUT_TYPE,
                "pulse_check_form": pulse_check_form,
                "bottle_exchange_form": bottle_exchange_form
            }
            return render(request, "wave/wave_for_participant.html", context)
        else:
            logout(request)
    return redirect(WAVE_REGISTRATION, wave_id=wave_id)

    
# def wave_for_participant (request, wave_id):
#     if request.user.is_authenticated and request.user.user_type == PARTICIPANT:
#         if request.user.wave_id == wave_id:
#             wave = Wave.objects.get(pk=wave_id)
#             form = BottleForm()
            
#             if request.method == 'POST':
#                 form = BottleForm(request.POST)
                
#                 if form.is_valid():
#                     form.save(commit=False)
#                     if request.POST.form_type == INPUT_TYPE.BOTTLE_EXCHANGE:
#                         form.input_type = INPUT_TYPE.BOTTLE_EXCHANGE
#                     else:
#                         form.input_type = INPUT_TYPE.PULSE_CHECK
#                         form.recipient_id = wave.facilitator_id
                        
#                     form.wave_id = wave_id;
#                     form.sender_id = request.user.id;
            
#             context = {
#                 "wave": wave,
#                 "INPUT_TYPE": INPUT_TYPE,
#                 "form": form,
#             }
#             return render(request, "wave/wave_for_participant.html", context)
#         else:
#             logout(request)
#     return redirect(WAVE_REGISTRATION, wave_id=wave_id)

def wave_for_presentation(request, wave_id):
    """ Display wave on screen for presentation, includes QR code and submitted messages for pulse check """
    if request.user.is_authenticated and request.user.user_type == FACILITATOR:
        facilitator_id = request.user.id
        wave = Wave.objects.get(pk=wave_id)
        if wave.facilitator_id != facilitator_id:
            return redirect(f"{settings.LOGIN_URL}")
        qr = create_wave_QR_code(request, wave_id)
        context = {
            "facilitator_id": facilitator_id,
            "wave": wave,
            "qr": qr
        }
        return render(request, "wave/wave_for_presentation.html", context)
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

   
# def training_user(request, user_id):
#     """Display training records and training hour totals for a specific employee."""
#     """Only superusers can view other user's records"""
#     if request.user.is_authenticated:
#         if request.user.is_staff:
#             employee = Employee.objects.get(pk=user_id)
#             user_trainings = Training.objects.filter(id=user_id)
#             total = services.get_total_number_of_training_hours(user_trainings)
#             ongoing_training = services.get_ongoing_training_hours(user_trainings)
#             completed_training = services.get_completed_training_hours(user_trainings)
#             context = {
#                 "user_id": user_id,
#                 "trainings": user_trainings,
#                 "employee": employee,
#                 "total_training": total,
#                 "ongoing_training": ongoing_training,
#                 "completed_training": completed_training
#             }
#             return render(request, "training/training_user.html", context)
        
#     return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    

# def training_employees(request):
#     """Display a list of all employees to view their training."""
#     """Only superusers can view other user's records"""
#     if request.user.is_authenticated:
#         if request.user.is_staff:
#             all_employees = Employee.objects.all()
#             context = {"employees": all_employees}
#             return render(request, "training/training_employees.html", context)
#     return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    

# def inbox(request):
#     """Display active messages for the current user."""
#     if request.user.is_authenticated:
#         user_id = request.user.id            
#         messages = Message.objects.filter(receiver_user_id=user_id, message_status=Message.ACTIVE)
#         context={
#             "messages": messages
#         }
#         return render(request, "messages/inbox.html", context)
#     else:
#         return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
    
# def archive(request):
#     """Display archived messages for the current user."""
#     if request.user.is_authenticated:
#         user_id = request.user.id            
#         messages = Message.objects.filter(receiver_user_id=user_id, message_status=Message.ARCHIVED)
#         context={
#             "messages": messages
#         }
#         return render(request, "messages/inbox.html", context)
#     else:
#         return redirect(f"{settings.LOGIN_URL}?next={request.path}")

  
# def message_status(request, message_id):
#     """Update the status of a message belonging to the current user."""
#     if request.user.is_authenticated:
#         user_id = request.user.id
#         if request.method == 'POST':
#             message_status = request.POST.get("message_status", 1)
#             message = Message.objects.get(pk=message_id)
#             if message.receiver_user_id != user_id:
#                 return redirect('inbox')
#             message.message_status = message_status
#             message.save()
#         return redirect('inbox')
#     else:
#         return redirect(f"{settings.LOGIN_URL}?next={request.path}")


# def outbox(request):
#     """Display messages sent by the current user."""
#     if request.user.is_authenticated:
#         user_id = request.user.id
#         messages = Message.objects.filter(sender_user_id=user_id)
#         context={
#             "messages": messages
#         }
#         return render(request, "messages/outbox.html", context)
#     else:
#         return redirect(f"{settings.LOGIN_URL}?next={request.path}")


# def message_detail(request, message_id):
#     """Display the details of a specific message."""
#     if request.user.is_authenticated:
#         message = Message.objects.get(id=message_id)
#         if message.receiver_user_id != request.user.id:
#             return redirect('inbox')
#         context={
#             "message": message
#         }
#         return render(request, "messages/message_detail.html", context)
#     else:
#         return redirect(f"{settings.LOGIN_URL}?next={request.path}")


# def compose(request):
#     """Display the message composition form and handle sending new messages."""    
#     if request.user.is_authenticated:
#         user_id = request.user.id
#         if request.method == 'POST':
#             form = MessageForm(request.POST, sender_id=user_id)
    
#             if form.is_valid():
#                 message = form.save(commit=False)
#                 message.sender_user_id = request.user.id
#                 message.message_status = Message.ACTIVE
#                 message.save()
#                 return redirect('inbox')
        
#         else:
#             form = MessageForm(sender_id=user_id)
        
#         return render(
#             request,
#             'messages/compose.html',
#             {'form': form}
#         )
#     else:
#         return redirect(f"{settings.LOGIN_URL}?next={request.path}")


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
            facilitator = Facilitator.objects.get(pk=request.user.id)
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
            participant = Participant.objects.get(pk=request.user.id)
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
            """ TODO: set this correctly """
            form.join_order = 1
            form.requested_follow_up = False
            form.user_type = PARTICIPANT
            form.is_staff = False
            form.is_superuser = False
    
            print('form', form.data)
            if form.is_valid():
                participant = form.save(commit=False)
                print('participant', participant)
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
            {'form': form, 'result': result, 'user_type': 'Participant'}
        )
    else:
        return redirect('/')