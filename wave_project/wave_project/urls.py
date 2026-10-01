"""
URL configuration for wave_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from wave_app import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from wave_app.constants import MY_WAVES_NAME, WAVE_NAME, WAVE_PRESENT_NAME, WAVE_REGISTRATION

urlpatterns = [
    path('', views.home_redirect),
    # path('/', views.home_redirect),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account_details/', views.account_details, name='account_details'),
    path('facilitator_registration/', views.facilitator_registration, name='facilitator_registration'),
    path('wave/registration/<int:wave_id>/', views.participant_registration, name= WAVE_REGISTRATION),
    path('wave/my-waves', views.my_waves, name=MY_WAVES_NAME),
    path('wave/<int:wave_id>/', views.wave_for_participant, name=WAVE_NAME),
    path('wave/create_wave/', views.create_wave, name='create_wave'),
    path('wave/present/<int:wave_id>/', views.wave_for_presentation, name=WAVE_PRESENT_NAME),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
        name='password_reset'
    ),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),
         name='password_reset_done'),
     
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
     
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
