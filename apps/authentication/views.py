

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm, UserUpdateForm, UserProfileForm, ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from apps.authentication.models import User
from django.contrib.auth import authenticate, login, logout
from ticketing.models import UserActivity 
# from user_agents import parse
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from user_agents import parse
import requests


def get_client_ip(request):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Log user login activity
                activity_details = f"User: {user.username} logged in"
                
                # Get the user agent from the request
                user_agent_string = request.META.get('HTTP_USER_AGENT', '')
                user_agent = parse(user_agent_string)

                # Get the user's IP address from the request
                ip_address = get_client_ip(request)
                
                # Make a request to the IPInfo API
                api_url = f"https://ipinfo.io/{ip_address}?token=0c00f775b92a27"

                response = requests.get(api_url)
                data = response.json()
                
                # Extract country and city information
                country = data.get('country')
                city = data.get('city')
                region = data.get('region')
    
    # Extract latitude and longitude from the 'loc' field
                loc = data.get('loc')
                if loc:
                  latitude, longitude = loc.split(',')
                else:
                 latitude = None
                 longitude = None
    
                device_name = user_agent_string
                
                # Create UserActivity instance with user agent, location, and other details
                UserActivity.objects.create(
                    user=user,
                    activity="User Login",
                    details=activity_details,
                    user_agent={
                        'is_mobile': user_agent.is_mobile,
                        'is_tablet': user_agent.is_tablet,
                        'browser_family': user_agent.browser.family,
                        'Device': device_name,
                        # ... other user agent attributes ...
                    },
                    ip_address=ip_address,
                    country=country,
                    city=city,
                    latitude=latitude,
                    longitude=longitude,
                    region=region,
                    timestamp=timezone.now()
                )

                return redirect("index")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})






# @login_required
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.warning(request, "An account with this email already exists.")
            else:
                # Create a new user instance
                user = form.save(commit=False)

                # Set the role based on toggle button values
                user.is_admin = request.POST.get('is_admin') == 'on'
                user.is_technician = request.POST.get('is_technician') == 'on'
                user.is_customer_care = request.POST.get('is_customer_care') == 'on'
                user.is_employee = request.POST.get('is_employee') == 'on'
                user.is_supervisor = request.POST.get('is_supervisor') == 'on'

                user.save()

                messages.info(request, "Account was created for " + str(user))
                return redirect('login')
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})



def logout_view(request):
    # Save the current user object before logging out
    user = request.user

    # Perform the logout operation
    logout(request)

    # Log user logout activity with the correct user information
    if user.is_authenticated:
        activity_details = f"User: {user.username} logged out"
        
        # Get the user agent from the request
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_string)

        # Get the user's IP address from the request
        ip_address = get_client_ip(request)
        
        # Make a request to the IPInfo API
        api_url = f"https://ipinfo.io/{ip_address}?token=0c00f775b92a27"

        response = requests.get(api_url)
        data = response.json()
        data = response.json()
                
                # Extract country and city information
        country = data.get('country')
        city = data.get('city')
        region = data.get('region')
    
    # Extract latitude and longitude from the 'loc' field
        loc = data.get('loc')
        if loc:
         latitude, longitude = loc.split(',')
        else:
         latitude = None
         longitude = None
    
        device_name = user_agent_string
        
        # Extract country and city information
        country = data.get('country')
        city = data.get('city')
        
        # Create UserActivity instance with user agent, location, and other details
        UserActivity.objects.create(
            user=user,
            activity="User Logout",
            details=activity_details,
            user_agent={
                'is_mobile': user_agent.is_mobile,
                'is_tablet': user_agent.is_tablet,
                'browser_family': user_agent.browser.family,
                'Device': device_name,
                # ... other user agent attributes ...
            },
            ip_address=ip_address,
            country=country,
            city=city,
            latitude=latitude,
            longitude=longitude,
            region=region,
            timestamp=timezone.now()
        )
    else:
        # Log activity with None for the user field to indicate that the user was not logged in
        activity_details = "User logged out (Not logged in)"
        
        # Get the user agent from the request
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_string)

        UserActivity.objects.create(
            user=None,
            activity="User Logout",
            details=activity_details,
            user_agent=user_agent  # Capture the user agent
        )

    return redirect('login')


@login_required
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_queue')  # Redirect to the user list page
    else:
        form = UserUpdateForm(instance=user)
    context = {'form': form, 'user': user}
    return render(request, 'update_user.html', context)


@login_required
def user_queue(request):
    activity_details = "Visited user queue page"
    
    # Get the user agent from the request
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    
    # Get the user's IP address from the request
    ip_address = get_client_ip(request)
    
    # Make a request to the IPInfo API
    api_url = f"https://ipinfo.io/{ip_address}?token=0c00f775b92a27"

    response = requests.get(api_url)
    data = response.json()
    
    # Extract country and city information
    country = data.get('country')
    city = data.get('city')
    
    device_name = user_agent_string
    # Create UserActivity instance with user agent, location, and other details
    UserActivity.objects.create(
        user=request.user,
        activity="Visited user queue page",
        details=activity_details,
        user_agent={
            'is_mobile': user_agent.is_mobile,
            'is_tablet': user_agent.is_tablet,
            'browser_family': user_agent.browser.family,
            'Device': device_name,
            # ... other user agent attributes ...
        },
        ip_address=ip_address,
        country=country,
        city=city,
        timestamp=timezone.now()
    )
    
    users = User.objects.all()

    # Convert the queryset to a list
    users_list = list(users)
    
    context = {'users': users_list}
    return render(request, 'user_queue.html', context)

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_admin)
def delete_user(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    user.delete()
    return redirect('user_queue') 




@login_required
def user_profile(request):
    user = request.user  
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)  
        if form.is_valid():
            form.save()
            print("Form is valid. Profile updated.")
            return redirect('index')  
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = UserProfileForm(instance=user)
    
    print("User:", user)
    print("Form:", form)

    context = {'form': form, 'user': user}
    return render(request, 'user_profile.html', context)


class ChangePasswordView(PasswordChangeView):
    template_name = 'change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('index')  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'change_password'  
        return context

