

from django.urls import path, re_path
from ticketing import views

from apps.home import views
from ticketing import views as ticketing_views

from .views import index

from apps.authentication import views as authenication_views
from django.contrib.auth import views as auth_views
from apps.authentication.forms import EmailValidationOnForgotPassword

urlpatterns = [

    # The home page
    path('', authenication_views.login_view, name='login'),
    #  path('add_ticket/', views.add_ticket, name='add_ticket'),
    path('index/', index, name='index'),
      
    # path('profile/', views.profile, name='profile'),
    path('tables/', views.tables, name='tables'),
    path('ticketing/add_ticket/', ticketing_views.add_ticket, name='add_ticket'),
    path('ticketing/accept_ticket/', ticketing_views.accept_ticket, name='accept_ticket'),
    path('ticketing/all_ticket_created/', ticketing_views.all_ticket_created, name='all_ticket_created'),
    path('ticketing/ticket_queue/', ticketing_views.ticket_queue, name='ticket_queue'),
    path('ticketing/user_activity_log/', ticketing_views.user_activity_log, name="user_activity_log"),
    path('ticketing/reject_ticket_form/<int:pk>/', ticketing_views.reject_ticket_form, name='reject_ticket_form'),
     path('ticketing/complete_ticket_customer/<int:pk>/', ticketing_views.complete_ticket_customer, name='complete_ticket_customer'),
    
    path('ticketing/ticket_to_claim_tech/', ticketing_views.ticket_to_claim_tech, name='ticket_to_claim_tech'),

    path('ticketing/technician_complete_ticket_admin/', ticketing_views.technician_complete_ticket_admin, name="technician_complete_ticket_admin"),

     path('ticketing/user_activities/', ticketing_views.user_activities_view, name='user_activities'),
    path('ticketing/customer_queue/', ticketing_views.customer_queue, name='customer_queue'),
    path('authentication/user_queue/', authenication_views.user_queue, name='user_queue'),
    path('ticketing/send_email/', ticketing_views.send_email, name='send_email'),
    path('authentication/update_user/<int:pk>/', authenication_views.update_user, name='update_user'),
     path('authentication/user_profile/', authenication_views.user_profile, name='user_profile'),
    
    path('authentication/user/<int:pk>/delete/', authenication_views.delete_user, name='delete_user'),
    
    path('authentication/change_password/', authenication_views.ChangePasswordView.as_view(), name='change_password'),
    
    path('api/create_ticket/', ticketing_views.create_ticket_api, name='create_ticket_api'),
   
    

    
     path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='password-reset.html',
        form_class=EmailValidationOnForgotPassword,
        success_url='/reset_password_sent/'
    ), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        success_url='/reset_password_complete/'
    ), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name="password_reset_complete"),
   
   

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]


