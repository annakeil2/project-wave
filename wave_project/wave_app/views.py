from django.shortcuts import render, redirect

from .models import Training, Message, Employee
from django.conf import settings
from .forms import TrainingForm, MessageForm, EmployeeForm, RegistrationForm
from . import services
from django.utils import timezone


def training_self(request):
    """Display the logged in user's training records and training hour totals."""
    if request.user.is_authenticated:
        user_id = request.user.id
        user_trainings = Training.objects.filter(user_id=user_id)
        total = services.get_total_number_of_training_hours(user_trainings)
        ongoing_training = services.get_ongoing_training_hours(user_trainings)
        completed_training = services.get_completed_training_hours(user_trainings)
        context = {
            "user_id": user_id,
            "trainings": user_trainings,
            "total_training": total,
            "ongoing_training": ongoing_training,
            "completed_training": completed_training
        }
        return render(request, "training/training_list.html", context)
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
   
def training_user(request, user_id):
    """Display training records and training hour totals for a specific employee."""
    """Only superusers can view other user's records"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            employee = Employee.objects.get(pk=user_id)
            user_trainings = Training.objects.filter(id=user_id)
            total = services.get_total_number_of_training_hours(user_trainings)
            ongoing_training = services.get_ongoing_training_hours(user_trainings)
            completed_training = services.get_completed_training_hours(user_trainings)
            context = {
                "user_id": user_id,
                "trainings": user_trainings,
                "employee": employee,
                "total_training": total,
                "ongoing_training": ongoing_training,
                "completed_training": completed_training
            }
            return render(request, "training/training_user.html", context)
        
    return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    

def training_employees(request):
    """Display a list of all employees to view their training."""
    """Only superusers can view other user's records"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            all_employees = Employee.objects.all()
            context = {"employees": all_employees}
            return render(request, "training/training_employees.html", context)
    return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    

def inbox(request):
    """Display active messages for the current user."""
    if request.user.is_authenticated:
        user_id = request.user.id            
        messages = Message.objects.filter(receiver_user_id=user_id, message_status=Message.ACTIVE)
        context={
            "messages": messages
        }
        return render(request, "messages/inbox.html", context)
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
    
def archive(request):
    """Display archived messages for the current user."""
    if request.user.is_authenticated:
        user_id = request.user.id            
        messages = Message.objects.filter(receiver_user_id=user_id, message_status=Message.ARCHIVED)
        context={
            "messages": messages
        }
        return render(request, "messages/inbox.html", context)
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

  
def message_status(request, message_id):
    """Update the status of a message belonging to the current user."""
    if request.user.is_authenticated:
        user_id = request.user.id
        if request.method == 'POST':
            message_status = request.POST.get("message_status", 1)
            message = Message.objects.get(pk=message_id)
            if message.receiver_user_id != user_id:
                return redirect('inbox')
            message.message_status = message_status
            message.save()
        return redirect('inbox')
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")


def outbox(request):
    """Display messages sent by the current user."""
    if request.user.is_authenticated:
        user_id = request.user.id
        messages = Message.objects.filter(sender_user_id=user_id)
        context={
            "messages": messages
        }
        return render(request, "messages/outbox.html", context)
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")


def message_detail(request, message_id):
    """Display the details of a specific message."""
    if request.user.is_authenticated:
        message = Message.objects.get(id=message_id)
        if message.receiver_user_id != request.user.id:
            return redirect('inbox')
        context={
            "message": message
        }
        return render(request, "messages/message_detail.html", context)
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")


def compose(request):
    """Display the message composition form and handle sending new messages."""    
    if request.user.is_authenticated:
        user_id = request.user.id
        if request.method == 'POST':
            form = MessageForm(request.POST, sender_id=user_id)
    
            if form.is_valid():
                message = form.save(commit=False)
                message.sender_user_id = request.user.id
                message.message_status = Message.ACTIVE
                message.save()
                return redirect('inbox')
        
        else:
            form = MessageForm(sender_id=user_id)
        
        return render(
            request,
            'messages/compose.html',
            {'form': form}
        )
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")


def training_form(request):
    """Display the training form and handle creation of a new training record."""    
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TrainingForm(request.POST)
    
            if form.is_valid():
                training = form.save(commit=False)
                training.user_id = request.user.id
                training.save()
                return redirect('training_self')
        
        else:
            form = TrainingForm()
        
        return render(
            request,
            'training/training_form.html',
            {'form': form}
        )
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    
    
def account_details(request):
    """Display and update the current user's employee account details."""    
    if request.user.is_authenticated:
        employee = Employee.objects.get(pk=request.user.id)
        result = None
        if request.method == 'POST':
            form = EmployeeForm(request.POST, instance=employee)
    
            if form.is_valid():
                employee = form.save(commit=False)
                employee.updated_date = timezone.now()
                employee.save()
                result = 'User updated'
        
        else:
            form = EmployeeForm(instance=employee)
        
        return render(
            request,
            'account_details.html',
            {'form': form, 'result': result}
        )
    else:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    

def registration(request):
    """Display the registration form and create a new employee account."""
    if request.user.is_authenticated == False:
        result = None
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
    
            if form.is_valid():
                employee = form.save()
                return redirect(f"/training/")
        
        else:
            form = RegistrationForm()
        
        return render(
            request,
            'registration.html',
            {'form': form, 'result': result}
        )
    else:
        return redirect(f"/training/")