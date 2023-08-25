from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
# from user.models import User
from .models import Ticket, UserActivity, Customer
from datetime import datetime
# from django.db.models import Q
from django.contrib.auth.decorators import login_required
from apps.authentication.models import User
# Create your views here.
from .forms import NewTicketForm, UpdateTicketForm, TechnicianFeedbackForm 
# from .filters import TicketFilter
import csv
# from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect, get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.core.mail import EmailMessage
from django.utils import timezone
from .forms import ConversationForm
# from django.utils.html import strip_tags



from django.core.mail import send_mail
from django.conf import settings
# from django.contrib.sites.shortcuts import get_current_site
# from twilio.rest import Client
from django.urls import reverse
# from .filters import TicketFilter, TicketFilterCustomer, TicketFilterAdmin
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os
from django.utils import timezone
from datetime import datetime
from django.utils.safestring import SafeText
from user_agents import parse
import requests

from django.http import FileResponse

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseNotFound, HttpResponse
import mimetypes
from user_agents import parse


def get_client_ip(request):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_ticket_url(request, ticket):
    domain = request.get_host()
    accept_url = reverse('accept_ticket', args=[ticket.pk])  
    url = f"http://{domain}{accept_url}"
    
    return url

from django.core.mail import send_mail
from django.conf import settings

# =================================================================== ADD TICKET -===========================================================
def add_ticket(request):
    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.status = 'Pending'
            form.save()
            
            # Log the ticket creation activity
            activity_details = f"Ticket ID: {ticket.ticket_number}, Customer: {ticket.customer}, Title: {ticket.title}"
            
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
                user=request.user,
                activity="Created A Ticket",
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
            
            # Send email to technician
            subject = 'New Ticket Assignment'
            from_email = settings.DEFAULT_FROM_EMAIL

            if ticket.assignee and ticket.assignee.email:
                technician_email = ticket.assignee.email

                # Render the email template with the relevant context data
                email_context = {
                    'technician': ticket.assignee,
                    'ticket': ticket,
                }
                message = render_to_string('email_templates/create_ticket.html', email_context)

                send_mail(subject, '', from_email, [technician_email], html_message=message)

                messages.success(request, "Ticket created successfully. A technician will be assigned soon!")
                return redirect('add_ticket')
            else:
                messages.warning(request, "Ticket created successfully. No technician assigned.")
                return redirect('add_ticket')
        else:
            messages.warning(request, "Something went wrong. Please check the form.")
    else:
        form = NewTicketForm()

    context = {'form': form}
    return render(request, 'add_ticket.html', context)
# =================================================== ACCEPT TICKET ===============================================================


def accept_ticket(request, pk):
    if request.user.is_technician:
        ticket = get_object_or_404(Ticket, pk=pk)
        ticket.assignee = request.user
        ticket.status = "In_Progress"
        ticket.accepted_date = datetime.now()
        ticket.save()

        # Log the ticket acceptance activity
        activity_details = f"Accepted Ticket: ID {ticket.ticket_number}, Customer: {ticket.customer}, Title: {ticket.title}"
        
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
            user=request.user,
            activity="Accepted Ticket",
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

        # Send email to customer care
        customer_care_email = ticket.created_by.email
        subject_care = 'Ticket Accepted'
        technician_name = request.user.get_username()
        email_context_care = {
            'technician_name': technician_name,
            'ticket': ticket,
        }
        message_care = render_to_string('email_templates/ticket_accepted_care.html', email_context_care)
        send_mail(subject_care, '', settings.DEFAULT_FROM_EMAIL, [customer_care_email], html_message=message_care)

        # Send email to customer
        customer_email = ticket.customer.email
        subject_customer = f'Update on Ticket: {ticket.customer.name}'
        email_context_customer = {
            'customer_name': ticket.customer.name,
            'ticket': ticket,
        }
        message_customer = render_to_string('email_templates/ticket_accepted_customer.html', email_context_customer)
        send_mail(subject_customer, '', settings.DEFAULT_FROM_EMAIL, [customer_email], html_message=message_customer)

        messages.success(request, "Ticket has been accepted successfully, kindly resolve as soon as possible!!")
        return redirect('ticket_in_progress')
    else:
        # Store the ticket ID in a session or temporary storage
        # request.session['pending_ticket_id'] = pk
        return redirect('ticket_queue')
    
# ================================================================== ALL TICKET CREATED ================================================



def all_ticket_created(request):
    user = request.user
    activity_details = "Visited all ticket created page"
    
    # Get the user agent from the request
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    UserActivity.objects.create(
        user=request.user,
        activity="Visited all ticket created page",
        details=activity_details,
        user_agent=user_agent,  # Capture the user agent
        timestamp=timezone.now()
    )

    ticket = Ticket.objects.filter(created_by=user).order_by("-date_created")
    
    # myfilter = TicketFilterCustomer(request.GET, queryset=ticket, request=request)

    # # Pagination
    # p = Paginator(myfilter.qs, 8) 
    # page = request.GET.get('page')
    # tickets_parginating = p.get_page(page)
    # nums = 'a' * tickets_parginating.paginator.num_pages

    # Update Ticket Form
    update_form = UpdateTicketForm()

    # if request.method == 'POST':
    #     if 'filterForm' in request.POST:
    #         # Handle filter form submission
    #         myfilter = TicketFilterCustomer(request.GET, queryset=ticket, request=request)
    #     elif 'updateForm' in request.POST:
    #         # Handle update form submission
    #         pk = request.POST.get('ticket_id')
    #         ticket_instance = get_object_or_404(Ticket, pk=pk)
    #         update_form = UpdateTicketForm(request.POST, instance=ticket_instance)
    #         if update_form.is_valid():
    #             update_form.save()
    #         return redirect('all_ticket_created')

    context = {
        'ticket': ticket,
        # 'myfilter': myfilter,
        # 'tickets_parginating': tickets_parginating,
        # 'nums': nums,
        'update_form': update_form,
    }

    return render(request, 'all_ticket_created.html', context)


# =====================================================TICKET QUEUE===========================================================

def ticket_queue(request):
    activity_details = "Visited ticket queue page"
    
    # Get the user agent from the request
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    UserActivity.objects.create(
        user=request.user,
        activity="Visited ticket queue page",
        details=activity_details,
        user_agent=user_agent,  # Capture the user agent
        timestamp=timezone.now()
    )

    ticket = Ticket.objects.filter(assignee=request.user, status='Pending').order_by('-date_created')
    context = {'ticket': ticket}
    return render(request, 'ticket_queue.html', context)

# =======================================TICKET IN PROGRESS=====================================================================

def ticket_in_progress(request):
    activity_details = "Visited ticket in progress page"
    
    # Get the user agent from the request
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    UserActivity.objects.create(
        user=request.user,
        activity="Visited ticket in progress page",
        details=activity_details,
        user_agent=user_agent,  # Capture the user agent
        timestamp=timezone.now()
    )

    ticket = Ticket.objects.filter(assignee=request.user, is_resolve=False, status="In_Progress").order_by('-accepted_date')
    context = {'ticket': ticket}
    return render(request, 'ticket_in_progress.html', context)










# ====================================================== CHAT ====================================================================



@login_required
def ticket_details(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    conversation = ticket.conversation or ""

    # Capture user activity for visiting the Ticket Details page
    activity_details = f"User visited Ticket Details page for Ticket ID: {ticket.ticket_number}"
    
    # Get the user agent from the request
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    UserActivity.objects.create(
        user=request.user,
        activity="Visited Ticket Details Page",
        details=activity_details,
        user_agent=user_agent  # Capture the user agent
    )

    if request.method == 'POST':
        form = ConversationForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.cleaned_data['conversation']
            attachment = request.FILES.get('attachment')
            if attachment:
                fs = FileSystemStorage()
                attachment_name = fs.save(attachment.name, attachment)
                attachment_url = fs.url(attachment_name)
            else:
                attachment_url = ""

            sender = request.user.username
            timestamp = timezone.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
            conversation += f"{timestamp} - {sender} - {message} - {attachment_url}\n"
            ticket.conversation = conversation
            ticket.conversation_date = timezone.now()
            ticket.save()
            form = ConversationForm()  
    else:
        form = ConversationForm()

    messages = []
    if conversation:
        lines = conversation.split('\n')
        for line in lines:
            parts = line.split(' - ')
            if len(parts) == 4:
                timestamp_str = parts[0]
                sender = parts[1]
                message = parts[2]
                attachment_url = parts[3]

                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f%z")
                except ValueError:
                    # Handle invalid timestamp format
                    timestamp = None

                messages.append({
                    'timestamp': timestamp,
                    'sender': sender,
                    'message': message,
                    'attachment_url': attachment_url,
                })

    context = {
        'ticket': ticket,
        'messages': messages,
        'form': form,
    }

    return render(request, 'ticket_details.html', context)



def download_attachment(request, attachment_url):
    attachment_path = os.path.join(settings.MEDIA_ROOT, attachment_url)

    if not os.path.exists(attachment_path):
        return HttpResponseNotFound("File not found")

    with open(attachment_path, 'rb') as attachment_file:
        response = FileResponse(attachment_file)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        return response




def send_message_view(request, ticket_id):
    ticket = Ticket.objects.get(ticket_number=ticket_id)
    sender = request.user.username
    message = request.POST['message']
    ticket.add_conversation_message(sender, message)


# ============================================================= CLOSE TICKET ========================================================





@login_required
def close_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.status = "TechComplete"
    ticket.is_resolve = True
    ticket.close_date = datetime.now()
    ticket.save()

    # Capture user activity
    activity_details = f"Ticket ID: {ticket.ticket_number}, Customer: {ticket.customer}, Title: {ticket.title}"

    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    ip_address = get_client_ip(request)
    
    api_url = f"https://ipinfo.io/{ip_address}?token=0c00f775b92a27"
    response = requests.get(api_url)
    data = response.json()
    
    country = data.get('country')
    city = data.get('city')
    region = data.get('region')
    
    loc = data.get('loc')
    if loc:
        latitude, longitude = loc.split(',')
    else:
        latitude = None
        longitude = None
    
    UserActivity.objects.create(
        user=request.user,
        activity="Close A Ticket",
        details=activity_details,
        user_agent={
            'is_mobile': user_agent.is_mobile,
            'is_tablet': user_agent.is_tablet,
            'browser_family': user_agent.browser.family,
            'Device': user_agent_string,
            # ... other user agent attributes ...
        },
        ip_address=ip_address,
        country=country,
        city=city,
        region=region,
        latitude=latitude,
        longitude=longitude,
        timestamp=timezone.now()
    )

    technician = request.user
    technician_assigned_tickets = Ticket.objects.filter(assignee=technician, status__in=["Pending", "In_Progress"])
    if not technician_assigned_tickets.exists():
        unassigned_ticket = Ticket.objects.filter(assignee__isnull=True).first()
        if unassigned_ticket:
            unassigned_ticket.assignee = technician
            unassigned_ticket.save()
            subject = 'Ticket Assigned to You'
            email_context = {
                'ticket': unassigned_ticket,
            }
            email_html_message = render_to_string('email_templates/ticket_assigned.html', email_context)
            email_plain_message = strip_tags(email_html_message)
            send_mail(subject, email_plain_message, settings.DEFAULT_FROM_EMAIL, [technician.email], html_message=email_html_message)

    subject = 'Ticket Completed'
    email_context = {
        'created_by_user': ticket.created_by,
        'ticket': ticket,
    }
    email_html_message = render_to_string('email_templates/ticket_closed.html', email_context)
    email_plain_message = strip_tags(email_html_message)
    send_mail(subject, email_plain_message, settings.DEFAULT_FROM_EMAIL, [ticket.created_by.email], html_message=email_html_message)

    messages.success(request, "Ticket has been resolved. An email notification has been sent to the ticket creator.")
    return redirect('ticket_queue')



# ================================================= ALL TICKET COMPLETED ==================================================================


def ticket_completed(request):
    activity_details = "Visited ticket completed page"
    
    # Get the user agent from the request
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    UserActivity.objects.create(
        user=request.user,
        activity="Visited ticket completed page",
        details=activity_details,
        user_agent=user_agent,  # Capture the user agent
        timestamp=timezone.now()
    )
    
    tickets = Ticket.objects.filter(status='Completed').order_by('-customer_approve_date')
    
    context = {'tickets': tickets}
    return render(request, 'ticket_completed.html', context)


# ==================================================== CANCEL TICKET ==============================================================

def complete_ticket_customer(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # Update ticket status and completion date
    ticket.status = "Completed"
    ticket.completed_on = datetime.now()
    ticket.save()
    
    # Capture user activity
    activity_details = f"Ticket ID: {ticket.ticket_number}, Customer: {ticket.customer}, Title: {ticket.title}"
    
    # Get the user agent from the request
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    UserActivity.objects.create(
        user=request.user,
        activity="Completed A Ticket",
        details=activity_details,
        user_agent=user_agent 
    )
    
    messages.success(request, "You have successfully completed this ticket!")
    return redirect('technician_complete_ticket')
 
 
# def export_csv_filter(request):
#     ticket = Ticket.objects.all()
#     myfilter = TicketFilter(request.GET, queryset=ticket).qs
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename= tickets.csv'
#     tickets = Ticket.objects.all()
#     writer = csv.writer(response)
#     writer.writerow(['Ticket Number', 'Customer Name', 'Ticket Title', 'Ticket Description', 'Assigned To', 'Created By', 'Ticket Status', 'Date Created'])
    
#     for ticket in myfilter:
#         writer.writerow([ticket.ticket_number, ticket.customer, ticket.title, ticket.description, ticket.assignee, ticket.created_by, ticket.status, ticket.date_created])
        
#     return response


# def export_pdf_filter(request):
#     ticket = Ticket.objects.all()
#     myfilter = TicketFilter(request.GET, queryset=ticket).qs

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=tickets.pdf'

#     doc = SimpleDocTemplate(response, pagesize=landscape(letter))
#     elements = []

#     data = [['Ticket Number', 'Customer Name', 'Ticket Title', 'Ticket Description', 'Assigned To', 'Created By', 'Ticket Status']]

#     for ticket in myfilter:
#         row = [ticket.ticket_number, ticket.customer, ticket.title, ticket.description, ticket.assignee, ticket.created_by, ticket.status]
#         data.append(row)

#     table = Table(data, repeatRows=1)

#     # Adjust column widths to fit the content
#     col_widths = [doc.width / len(data[0]) for _ in data[0]]
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), '#CCCCCC'),
#         ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 12),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), '#ffffff'),
#         ('GRID', (0, 0), (-1, -1), 1, '#000000'),
#         ('COLWIDTH', (0, 0), (-1, -1), col_widths),
#     ]))

#     elements.append(table)

#     doc.build(elements)
#     return response



    



# ================================================TICKET REPORT ADMIN=============================================================


def ticket_report(request):
    # Capture user activity for visiting the Ticket Report page
    activity_details = "Visited all ticket page"
    
    # Get the user agent from the request
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    UserActivity.objects.create(
        user=request.user,
        activity="Visited all ticket page",
        details=activity_details,
        user_agent=user_agent,  # Capture the user agent
        timestamp=timezone.now()
    )
    
    tickets = Ticket.objects.all().order_by('-date_created')

    context = {'tickets': tickets}
    return render(request, 'ticket_report.html', context)


# ===================================================== UPDATE TICKET ================================================================

def update_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    if ticket.status == 'Pending':
        if request.method == 'POST':
            form = UpdateTicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
            
                # Capture user activity
                activity_details = f"Ticket ID: {ticket.ticket_number}, Customer: {ticket.customer}, Title: {ticket.title}"
                
                # Get the user agent from the request
                user_agent = request.META.get('HTTP_USER_AGENT', '')

                UserActivity.objects.create(
                    user=request.user,
                    activity="Updated A Ticket",
                    details=activity_details,
                    user_agent=user_agent  # Capture the user agent
                )

                # Check if the assignee field is present in the form's cleaned_data
                if 'assignee' in form.cleaned_data:
                    new_assignee = form.cleaned_data['assignee']
                    
                    # Send email to the new assignee
                    subject = 'You have been assigned a new ticket'
                    html_message = render_to_string('email_templates/new_ticket_assigned.html', {'ticket': ticket})
                    plain_message = strip_tags(html_message)
                    from_email = 'your_email@example.com'
                    to_email = new_assignee.email
                    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

                messages.success(request, "Ticket Successfully updated!!")
                return redirect('index')
            else:
                messages.warning(request, "Something went wrong, please check the output")
        else:
            form = UpdateTicketForm(instance=ticket)
         
        context = {'form': form}
        return render(request, 'update_ticket.html', context)
       
       
       
       

@login_required
def technician_complete_ticket(request):
    user = request.user

    # Capture user activity for visiting the Technician Complete page
    activity_details = "User visited Technician Complete page"
    
    # Get the user agent from the request
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    UserActivity.objects.create(
        user=user,
        activity="Visited Technician Complete Page",
        details=activity_details,
        user_agent=user_agent,  # Capture the user agent
        timestamp=timezone.now()
    )

    tickets = Ticket.objects.filter(status='TechComplete', created_by=user).order_by('-close_date')
    context = {'tickets': tickets}
    return render(request, 'technician_complete_ticket.html', context)


@login_required
def technician_complete_ticket_admin(request):
    # Capture user activity for visiting the Technician Complete page
    activity_details = "User visited Technician Complete page"
    
    # Get the user agent from the request
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    UserActivity.objects.create(
        user=request.user,
        activity="Visited Technician Complete Page",
        details=activity_details,
        user_agent=user_agent,  # Capture the user agent
        timestamp=timezone.now()
    )

    tickets = Ticket.objects.filter(status='TechComplete').order_by('-close_date')
    context = {'tickets': tickets}
    return render(request, 'technician_complete_ticket_admin.html', context)



from .forms import customerRejectionForm

def send_rejection_email(ticket):
    created_by_user = ticket.created_by
    customer_care_email = created_by_user.email 
    subject_care = 'Ticket Rejected'
    technician_name = ticket.assignee
    message_care = f'The ticket "{ticket.title}" that was assigned to {technician_name} has been rejected by the customer. Reason: {ticket.rejection_reason}'
    send_mail(subject_care, message_care, settings.DEFAULT_FROM_EMAIL, [customer_care_email])


def reject_ticket_form(request, pk):
    if request.method == 'POST':
        form = customerRejectionForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the rejection form data and send the rejection email
            ticket = Ticket.objects.get(pk=pk)
            rejection_reason = form.cleaned_data['customer_remark']
            attachments = form.cleaned_data['customer_attachments']

         
            ticket.rejection_reason = rejection_reason
            ticket.attachments = attachments
            ticket.status =  "CustomerDisproved"
            
            ticket.rejected_date = datetime.now()
            ticket.save()

            # Send rejection email to customer care
            send_rejection_email(ticket)

            # Return a simple thank-you message
            return HttpResponse("Thank you for your feedback. We will get back to you soon.")
    else:
        form = customerRejectionForm()

    return render(request, 'reject_ticket_form.html', {'form': form})



def complete_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.status = 'Completed'
    ticket.save()
   
    return HttpResponse("Work completion confirmed. Thank you!")




def send_completion_email(ticket):
    customer_email = ticket.customer.email
    domain = 'localhost:8000'

    # Build the completion URL for marking the ticket as completed
    completion_url = f"http://{domain}{reverse('complete_ticket', args=[ticket.pk])}"

    # Build the rejection URL for the customer to click
    rejection_url = f"http://{domain}{reverse('reject_ticket_form', args=[ticket.pk])}"

    # Compose the email subject
    email_subject = 'Ticket Completion Notification'

    # # Render the HTML email template
    email_html_message = render_to_string('completion_email.html', {'completion_url': completion_url, 'rejection_url': rejection_url})

    # Strip HTML tags to create a plain text email message
    email_plain_message = strip_tags(email_html_message)

    # Make the URLs clickable in the HTML email
    email_html_message = email_html_message.replace(completion_url, f'<a href="{completion_url}">{completion_url}</a>')
    email_html_message = email_html_message.replace(rejection_url, f'<a href="{rejection_url}">{rejection_url}</a>')

    # Send the email
    send_mail(email_subject, email_plain_message, settings.DEFAULT_FROM_EMAIL, [customer_email], html_message=mark_safe(email_html_message))



    # Redirect or display a success message
    
def customer_approve(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not ticket.status == "Pending" or ticket.status == "In_Progress":
        ticket.status = "CustomerApproved"
        ticket.is_resolve = True
        ticket.customer_approve_date = datetime.now()
        ticket.save()

        # Capture user activity
        activity_details = f"Ticket ID: {ticket.ticket_number}, Customer: {ticket.customer}, Title: {ticket.title}"
        
        # Get the user agent from the request
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        UserActivity.objects.create(
            user=request.user,
            activity="Sent Ticket for customer Approver",
            details=activity_details,
            user_agent=user_agent  # Capture the user agent
        )

        # Send completion email to customer
        send_completion_email(ticket)

        messages.success(request, "Ticket has been sent for customer approver. An email has been sent to the customer.")
        return redirect('technician_complete_ticket')
    else:
        messages.warning(request, "You can't send a pending ticket or ticket in progress for customer confirmation!")
        return redirect('technician_complete_ticket')


  
    

# ================================================= UNASSIGNED TICKET ===========================================================


def ticket_to_claim_tech(request):
    
    ticket = Ticket.objects.filter(assignee__isnull=True).order_by('-date_created')
    
    context = {'ticket': ticket}
    return render(request, 'ticket_to_claim_tech.html', context)



def user_activity_log(request):
    user_activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'user_activity_log.html', {'user_activities': user_activities})


def user_activities_view(request):
    # Get all users
    users = User.objects.all()

    # Get the selected user ID from the request parameters
    user_id = request.GET.get('user')

    # Initialize activities to show all if no user is selected
    activities = UserActivity.objects.all().order_by('-timestamp')

    # If a user ID is provided, filter activities for that user
    if user_id:
        selected_user = get_object_or_404(User, id=user_id)
        activities = UserActivity.objects.filter(user=selected_user)

    context = {
        'users': users,
        'activities': activities,
    }

    return render(request, 'user_activities.html', context)





import ipinfo
from ipinfo import getHandler



def customer_queue(request):
    activity_details = "Visited customer queue page"
    
    # Get the user agent from the request
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    
    # Get the user's IP address from the request
    ip_address = get_client_ip(request)
    
    # Make a request to the IPInfo API
    api_url = f"https://ipinfo.io/{ip_address}?token=0c00f775b92a27"
    response = requests.get(api_url)
    data = response.json()
    
    print("API Response:", response.text)  # Print the entire API response
    print("Data:", data)  # Print the parsed JSON data
    
    # Extract country and city information
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
        user=request.user,
        activity="Visited customer queue page",
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
    
    customers = Customer.objects.all()
    
    context = {'customers': customers}
    return render(request, 'customer_queue.html', context)










@login_required
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_profile.html', {'user': user})


def send_email(request):
    if request.method == 'POST':
        to_email = request.POST.get('to')
        cc_email = request.POST.get('cc')
        subject = request.POST.get('subject')
        message = request.POST.get('composer')
        from_email = settings.DEFAULT_FROM_EMAIL  # Use the configured 'from' email

        if cc_email:
            cc_email = cc_email.split(',')
            # Send the email with CC recipients
            email = EmailMessage(subject, message, from_email, [to_email], cc=cc_email)
        else:
            # Send the email without CC recipients
            email = EmailMessage(subject, message, from_email, [to_email])

        email.send()
        
        # Capture user activity
        activity_details = f"Email sent to: {to_email}, CC: {cc_email}, Subject: {subject}"
        UserActivity.objects.create(user=request.user, activity="Email Sent", details=activity_details, timestamp=timezone.now())

    
    return render(request, 'customer_queue.html', {'customer': Customer.objects.all()})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TicketSerializer

from django.utils import timezone

@api_view(['POST'])
def create_ticket_api(request):
    if request.method == 'POST':
        # Set the created_by field to the user with primary key 1
        request.data['created_by'] = 2  # Replace 1 with the actual primary key of the user you want

        # Set the current timestamp as the ticket's date_created
        request.data['date_created'] = timezone.now()

        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            ticket = serializer.save()

            # Your existing code to log the ticket creation activity, send email, etc.

            return Response({'message': 'Ticket created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

