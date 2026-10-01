from django.shortcuts import render, redirect

from .models import Wave, Bottle, Announcement, Facilitator, Participant, FACILITATOR, PARTICIPANT
from django.conf import settings
from .forms import WaveForm, FacilitatorRegistrationForm, ParticipantRegistrationForm
# from . import services
from django.utils import timezone
from .constants import MY_WAVES_NAME, WAVE_NAME


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
            "my_waves": my_waves,
        }
        return render(request, "wave/my_waves.html", context)
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
def wave_for_participant (request):
    return render(request, "wave/my_waves.html")


   
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


def wave_form(request):
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
                employee = form.save()
                return redirect(MY_WAVES_NAME)
        
        else:
            form = FacilitatorRegistrationForm()
        
        return render(
            request,
            'registration.html',
            {'form': form, 'result': result}
        )
    else:
        return redirect('')
    
    
def participant_registration(request):
    """ Display the registration form and create a new participant account """
    wave_id = request.GET.get('wave_id', None)
    if request.user.is_authenticated == False and wave_id != None:
        result = None
        if request.method == 'POST':
            form = ParticipantRegistrationForm(wave_id, request.POST)
    
            if form.is_valid():
                employee = form.save()
                return redirect('WAVE_NAME', wave_id=wave_id)
        
        else:
            form = ParticipantRegistrationForm()
        
        return render(
            request,
            'registration.html',
            {'form': form, 'result': result}
        )
    else:
        return redirect('')