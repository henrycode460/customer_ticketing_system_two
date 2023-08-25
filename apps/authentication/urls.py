
from django.urls import path
from .views import login_view, register_user, logout_view, update_user, delete_user, user_queue, user_profile , ChangePasswordView
from django.contrib.auth import views as auth_views
from apps.authentication.forms import EmailValidationOnForgotPassword





urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
   path('logout/', logout_view, name='logout'),
   path('update_user/<int:pk>/', update_user, name='update_user'),
   path('user/<int:pk>/delete/', delete_user, name='delete_user'),
   path('user_queue/', user_queue, name='user_queue'),
   path('user_profile/', user_profile, name='user_profile'),
     path('change_password/', ChangePasswordView.as_view(), name='change_password'),
   
   
   
   
   
    
]
