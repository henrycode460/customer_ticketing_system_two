

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template import loader
from django.urls import reverse
import json
from django.shortcuts import render, redirect

from ticketing.models import Ticket
from ticketing.models import Ticket
from django.shortcuts import render
from django.db.models import Count
from datetime import datetime
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth
# from dateutil.relativedelta import relativedelta


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     try:
#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         elif load_template == 'ticketing':
#             context['segment'] = load_template
#             return render(request, 'ticketing/add_ticket.html', context)

#         context['segment'] = load_template

#         html_template = loader.get_template('home/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:
#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))




    






def tables(request):
    
    
    
    return render(request, 'tables.html')

def index( request):
    
    ticketAdmin = Ticket.objects.filter(status="Pending").order_by('-date_created')[:5]
    ticketAdminstration = Ticket.objects.filter(status="Pending").order_by('-date_created')
    ticketFiveCompleted = Ticket.objects.filter(status="Completed").order_by('-customer_approve_date')[:5]
    ticketInprogressAdmin = Ticket.objects.filter(status="In_Progress").order_by('-accepted_date')
    ticketInpostpone = Ticket.objects.filter(status="Postpone")
    ticketCancel = Ticket.objects.filter(status="Cancel")
    ticketUnassigned = Ticket.objects.filter(assignee__isnull=True).order_by('-date_created')
    ticketCustApprovers = Ticket.objects.filter(status="CustomerApproved").order_by('-customer_approve_date')
    
    tickets = Ticket.objects.filter(assignee=request.user, status="Pending").order_by('-date_created')
    
    
    
    #Integration for customer care
    user = request.user
    ticketpendingCS = Ticket.objects.filter(status="Pending", created_by=user).order_by('-date_created')
    ticketCS = Ticket.objects.filter(status="Pending", created_by=user).order_by('-date_created')
    ticketAwaitingCusotmerApp = Ticket.objects.filter(status="CustomerApproved", created_by=user)
    ticketInprogress = Ticket.objects.filter(status="In_Progress", created_by=user).order_by('-accepted_date')
    
    # ===================================== TECHNICIAN TICKET STATUS =================================================
    
    ticketInprogresstech = Ticket.objects.filter(status="In_Progress", assignee=user).order_by('-accepted_date')
    ticketAwaitingCusotmerAppTech = Ticket.objects.filter(status="CustomerApproved", assignee=user).order_by('-customer_approve_date')
    ticketPendingtech = Ticket.objects.filter(status="Pending", assignee=user).order_by('-date_created')
    ticketPostponetech = Ticket.objects.filter(status="Postpone", assignee=user).order_by('-postpone_date')
    
    ticketunassigned = Ticket.objects.filter(assignee__isnull=True, created_by=user).order_by('-date_created')
    ticketunassignedFive = Ticket.objects.filter(assignee__isnull=True, created_by=user).order_by('-date_created')[:5]
    
    
    # chart------------------------------------------
    
    pending_no = Ticket.objects.filter(status="Pending").count()
    pending_no = int(pending_no)
    
    ticketUnassigned_admin = Ticket.objects.filter(assignee__isnull=True).count()
    ticketUnassigned_admin = int(ticketUnassigned_admin)
    
    ticketCustApprover = Ticket.objects.filter(status="CustomerApproved").count()
    ticketCustApprover = int(ticketCustApprover)
    
    inprogress_no = Ticket.objects.filter(status="In_Progress").count()
    inprogress_no = int( inprogress_no)
    
    cancel_no = Ticket.objects.filter(status="CustomerDisproved").count()
    cancel_no = int( cancel_no)
    
    postpone_no = Ticket.objects.filter(status="Completed").count()
    postpone_no = int(postpone_no)
    
    ticker_created_no = Ticket.objects.filter(status="Pending", created_by=user).count()
    ticker_created_no = int(ticker_created_no)
    
    ticket_unassigned_no = Ticket.objects.filter(assignee__isnull=True, created_by=user).count()
    ticket_unassigned_no = int( ticket_unassigned_no)
    
    ticket_customerapprover_no = Ticket.objects.filter(status="CustomerApproved", created_by=user).count()
    ticket_customerapprover_no = int( ticket_customerapprover_no)
    
    ticket_inprogress_no = Ticket.objects.filter(status="In_Progress", created_by=user).count()
    ticket_inprogress_no = int( ticket_inprogress_no)
    
    ticket_inprogresstech_no = Ticket.objects.filter(status="In_Progress", assignee=user).count()
    ticket_inprogresstech_no = int(ticket_inprogresstech_no)
    
    ticket_pendingtech_no = Ticket.objects.filter(status="Pending", assignee=user).count()
    ticket_pendingtech_no = int(ticket_pendingtech_no)
    
    ticket_postpone_no = Ticket.objects.filter(status="Postpone", assignee=user).count()
    ticket_postpone_no  = int(ticket_postpone_no )
    
    status_list_Admin = ['Pending', 'In_Progress', 'Cust. Disapproved', 'Completed', 'Ticket Unassigned', 'Waiting Customer Approver']
    status_number_Admin = [pending_no, inprogress_no, cancel_no, postpone_no, ticketUnassigned_admin, ticketCustApprover ]
    
    status_list = ['Ticket Pending', 'Unassigned Ticket', 'Ticket Customer Approver', 'Ticket In Progress', 'Ticket Pending', 'Ticket In Progress']
    status_number = [ticker_created_no, ticket_unassigned_no, ticket_customerapprover_no, ticket_inprogress_no, ticket_pendingtech_no,  ticket_inprogresstech_no   ]
    
    status_list_tech = [ 'Ticket Pending', 'Ticket In Progress', 'Ticket Postpone']
    status_number_tech = [ticket_pendingtech_no,  ticket_inprogresstech_no, ticket_postpone_no ]
    
    # pie chart
    
    top_customers = Ticket.objects.filter(title='Support').values('customer__name').annotate(support_count=Count('customer')).order_by('-support_count')[:5]

    # Extract the customer names and support counts
    top_customer_names = [customer['customer__name'] for customer in top_customers]
    support_counts = [customer['support_count'] for customer in top_customers]

    # Prepare the data for the pie chart
    labels = top_customer_names
    data = support_counts
    colors = ['#FF6384', '#36A2EB', '#FFCE56', '#32CD32', '#FF9900']


    
    #chart end--------------------------------------------------------
    
    # ============================================= TICKET PERCENTAGE PENDING ============================================================
    
   # Define the status and the month for which you want to calculate the percentage
    status = 'Pending'
    month = datetime.now() - timedelta(days=30)  # One month ago
    # Retrieve the logged-in user
    user = request.user
    # Retrieve the total number of tickets with the desired status for the logged-in user
    total_status_tickets = Ticket.objects.filter(created_by=user, status=status).count()
    # Retrieve the total number of tickets created by the logged-in user in the specified month
    total_month_tickets = Ticket.objects.filter(created_by=user, date_created__gte=month).count()
    # Calculate the percentage
    percentage = (total_status_tickets / total_month_tickets) * 100 if total_month_tickets != 0 else 0
    
    # ============================================= TICKET PERCENTAGE INPROGRESS ============================================================
    
       # Define the status and the month for which you want to calculate the percentage
    status = 'In_Progress'
    month = datetime.now() - timedelta(days=30)  # One month ago

    # Retrieve the logged-in user
    user = request.user

    # Retrieve the total number of tickets with the desired status for the logged-in user
    total_status_tickets = Ticket.objects.filter(created_by=user, status=status).count()

    # Retrieve the total number of tickets created by the logged-in user in the specified month
    total_month_tickets = Ticket.objects.filter(created_by=user, date_created__gte=month).count()

    # Calculate the percentage
    percentageProgress = (total_status_tickets / total_month_tickets) * 100 if total_month_tickets != 0 else 0
    
     # ============================================= TICKET PERCENTAGE CUSTOME APPROVER ============================================================
    
       # Define the status and the month for which you want to calculate the percentage
    status = 'CustomerApproved'
    month = datetime.now() - timedelta(days=30)  # One month ago

    # Retrieve the logged-in user
    user = request.user

    # Retrieve the total number of tickets with the desired status for the logged-in user
    total_status_tickets = Ticket.objects.filter(created_by=user, status=status).count()

    # Retrieve the total number of tickets created by the logged-in user in the specified month
    total_month_tickets = Ticket.objects.filter(created_by=user, date_created__gte=month).count()

    # Calculate the percentage
    percentageCustAppro = (total_status_tickets / total_month_tickets) * 100 if total_month_tickets != 0 else 0
    
        # ============================================= TICKET PERCENTAGE UNASSIGNED ============================================================
    
    # Retrieve the logged-in user
    user = request.user

# Retrieve the total number of tickets with the desired status for the logged-in user
    total_status_tickets = Ticket.objects.filter(created_by=user, assignee__isnull=True).count()

# Retrieve the total number of tickets created by the logged-in user in the specified month
    total_month_tickets = Ticket.objects.filter(created_by=user, date_created__gte=month).count()

# Calculate the percentage
    percentageUnassigned = (total_status_tickets / total_month_tickets) * 100 if total_month_tickets != 0 else 0
    
    
# ===================================== TOTAL TICKET CREATED FOR EACH MONTH ==============================================

# Retrieve the ticket data for each month
    ticket_data = Ticket.objects.annotate(month=TruncMonth('date_created')).values('month').annotate(count=Count('ticket_number')).values_list('count', flat=True)



    # ============================================= TICKET PERCENTAGE PENDING TECH ============================================================
    
   # Define the status and the month for which you want to calculate the percentage
    status = 'Pending'
    month = datetime.now() - timedelta(days=30)  # One month ago
    # Retrieve the logged-in user
    user = request.user
    # Retrieve the total number of tickets with the desired status for the logged-in user
    total_status_tickets = Ticket.objects.filter(assignee=user, status=status).count()
    # Retrieve the total number of tickets created by the logged-in user in the specified month
    total_month_tickets = Ticket.objects.filter(assignee=user, date_created__gte=month).count()
    # Calculate the percentage
    percentageTech = (total_status_tickets / total_month_tickets) * 100 if total_month_tickets != 0 else 0
    
      # ============================================= TICKET PERCENTAGE INPROGRESS TECH ============================================================
    
       # Define the status and the month for which you want to calculate the percentage
    status = 'In_Progress'
    month = datetime.now() - timedelta(days=30)  # One month ago

    # Retrieve the logged-in user
    user = request.user

    # Retrieve the total number of tickets with the desired status for the logged-in user
    total_status_tickets = Ticket.objects.filter(assignee=user, status=status).count()

    # Retrieve the total number of tickets created by the logged-in user in the specified month
    total_month_tickets = Ticket.objects.filter(assignee=user, date_created__gte=month).count()

    # Calculate the percentage
    percentageProgressTech = (total_status_tickets / total_month_tickets) * 100 if total_month_tickets != 0 else 0
    
      # ============================================= TICKET PERCENTAGE CUSTOME APPROVER TECH ============================================================
    
       # Define the status and the month for which you want to calculate the percentage
    status = 'CustomerApproved'
    month = datetime.now() - timedelta(days=30)  # One month ago

    # Retrieve the logged-in user
    user = request.user

    # Retrieve the total number of tickets with the desired status for the logged-in user
    total_status_tickets = Ticket.objects.filter(assignee=user, status=status).count()

    # Retrieve the total number of tickets created by the logged-in user in the specified month
    total_month_tickets = Ticket.objects.filter(assignee=user, date_created__gte=month).count()

    # Calculate the percentage
    percentageCustApproTech = (total_status_tickets / total_month_tickets) * 100 if total_month_tickets != 0 else 0
    
    
        # ============================================= TICKET PERCENTAGE UNASSIGNED TECH ============================================================
    
    # Retrieve the logged-in user
    user = request.user

# Retrieve the total number of tickets with the desired status for the logged-in user
    total_status_tickets = Ticket.objects.filter(assignee__isnull=True).count()

# Retrieve the total number of tickets created by the logged-in user in the specified month
    total_month_tickets = Ticket.objects.filter(date_created__gte=month).count()

# Calculate the percentage
    percentageUnassignedAll = (total_status_tickets / total_month_tickets) * 100 if total_month_tickets != 0 else 0
    
# ============================================= TICKET PERCENTAGE PENDING ADMIN ============================================================
    
   # Define the status and the month for which you want to calculate the percentage
    status = 'Pending'
    month = datetime.now() - timedelta(days=30)  # One month ago
    # Retrieve the logged-in user
    user = request.user
    # Retrieve the total number of tickets with the desired status for the logged-in user
    total_status_tickets = Ticket.objects.filter(status=status).count()
    # Retrieve the total number of tickets created by the logged-in user in the specified month
    total_month_tickets = Ticket.objects.filter(date_created__gte=month).count()
    # Calculate the percentage
    percentageAdmin = (total_status_tickets / total_month_tickets) * 100 if total_month_tickets != 0 else 0
    
 # ============================================= TICKET PERCENTAGE INPROGRESS ADMIN ============================================================
    
       # Define the status and the month for which you want to calculate the percentage
    status = 'In_Progress'
    month = datetime.now() - timedelta(days=30)  # One month ago

    # Retrieve the logged-in user
    user = request.user

    # Retrieve the total number of tickets with the desired status for the logged-in user
    total_status_tickets = Ticket.objects.filter( status=status).count()

    # Retrieve the total number of tickets created by the logged-in user in the specified month
    total_month_tickets = Ticket.objects.filter(date_created__gte=month).count()

    # Calculate the percentage
    percentageProgressAdmin = (total_status_tickets / total_month_tickets) * 100 if total_month_tickets != 0 else 0
    
  # ============================================= TICKET PERCENTAGE CUSTOME APPROVER ADMIN ============================================================
    
       # Define the status and the month for which you want to calculate the percentage
    status = 'CustomerApproved'
    month = datetime.now() - timedelta(days=30)  # One month ago

    # Retrieve the logged-in user
    user = request.user

    # Retrieve the total number of tickets with the desired status for the logged-in user
    total_status_tickets = Ticket.objects.filter(status=status).count()

    # Retrieve the total number of tickets created by the logged-in user in the specified month
    total_month_tickets = Ticket.objects.filter(date_created__gte=month).count()

    # Calculate the percentage
    percentageCustApproAdmin = (total_status_tickets / total_month_tickets) * 100 if total_month_tickets != 0 else 0
    


        # ============================================= TICKET PERCENTAGE UNASSIGNED ADMI ============================================================
    
    # Retrieve the logged-in user
    user = request.user

# Retrieve the total number of tickets with the desired status for the logged-in user
    total_status_tickets = Ticket.objects.filter(assignee__isnull=True).count()

# Retrieve the total number of tickets created by the logged-in user in the specified month
    total_month_tickets = Ticket.objects.filter(date_created__gte=month).count()

# Calculate the percentage
    percentageUnassignedAll = (total_status_tickets / total_month_tickets) * 100 if total_month_tickets != 0 else 0
    
    
    #======================================================= ticket compelte ===========================================================
 # Fetch the data from the database and count the number of "Completed" tickets for each assignee
    assignees_data = Ticket.objects.filter(status='Completed').values('assignee__username').annotate(num_completed=Count('assignee'))

    # Sort the data by the number of completed tickets (descending order)
    assignees_data = assignees_data.order_by('-num_completed')[:5]

    # Convert the queryset to a list of dictionaries
    assignees_list = list(assignees_data)

    # Convert the data to JSON format for passing to the template
    assignees_list_json = json.dumps(assignees_list)

    
# ====================================================== CHAT NOTIFICATION =========================================================

    chat_messages = []
    tickets = Ticket.objects.all()

    for ticket in tickets:
     conversation = ticket.conversation
     if conversation:
        lines = conversation.split('\n')
        for line in lines:
            parts = line.split(' - ')
            if len(parts) == 4:
                sender = parts[1]
                message = parts[2]
                attachment_url = parts[3]

                if sender != request.user.username:
                    chat_message = {
                        'ticket': ticket,
                        'sender': sender,
                        'message': message,
                        'attachment_url': attachment_url,
                    }
                    # Insert the new chat_message at the beginning of the list
                    chat_messages.insert(0, chat_message)

# Limit the number of chat_messages to display
    chat_messages = chat_messages[:6]

    notification_count = len(chat_messages)


        
    
    
    context = {'tickets': tickets , 'ticketUnassigned': ticketUnassigned,  'ticket': ticket, 'ticketunassigned': ticketunassigned,'ticker_created_no': ticker_created_no, 'ticket_unassigned_no': ticket_unassigned_no, 'ticket_customerapprover_no': ticket_customerapprover_no, 'ticket_inprogress_no': ticket_inprogress_no, 'status_list': status_list, 'status_number': status_number, 
                'status_list_tech': status_list_tech , 'status_number_tech': status_number_tech ,'ticketAwaitingCusotmerApp': ticketAwaitingCusotmerApp, 'ticketInprogress': ticketInprogress, 'ticket_pendingtech_no': ticket_pendingtech_no, 
                'ticket_inprogresstech_no': ticket_inprogresstech_no, 'ticketInprogresstech' : ticketInprogresstech,
                'ticketPendingtech': ticketPendingtech,  'ticket_postpone_no': ticket_postpone_no,
                'ticketPostponetech': ticketPostponetech, 'status_list_Admin': status_list_Admin, 
                'status_number_Admin': status_number_Admin, 'pending_no' : pending_no, 
                'ticketUnassigned': ticketUnassigned, 
                'ticketCustApprover': ticketCustApprover, 'inprogress_no': inprogress_no, 
                'cancel_no' : cancel_no, 'postpone_no': postpone_no, 
                'ticketAdmin': ticketAdmin, 'ticketInprogressAdmin': ticketInprogressAdmin, 
                'ticketInpostpone': ticketInpostpone, 'ticketCancel': ticketCancel , 
                 'ticketUnassigned_admin': ticketUnassigned_admin, 
                 'percentage': percentage, 'percentageProgress': percentageProgress, 
                 'percentageCustAppro': percentageCustAppro, 
                 'percentageUnassigned': percentageUnassigned, 'ticket_data': ticket_data, 
                 'ticketFiveCompleted': ticketFiveCompleted, 
                 'ticketAwaitingCusotmerAppTech': ticketAwaitingCusotmerAppTech,
                 'percentageTech':percentageTech, 'percentageProgressTech': percentageProgressTech, 
                 'percentageCustApproTech': percentageCustApproTech, 
                 'percentageUnassignedAll':percentageUnassignedAll, 
                 'ticketAdminstration': ticketAdminstration, 
                 'ticketCustApprovers': ticketCustApprovers, 
                 'percentageAdmin': percentageAdmin, 
                 'percentageProgressAdmin': percentageProgressAdmin, 
                 'percentageCustApproAdmin': percentageCustApproAdmin, 
                 'ticketunassignedFive': ticketunassignedFive, 
                 'chat_messages': chat_messages, 'ticketCS ': ticketCS, 'notification_count': notification_count, 
                 'labels': labels, 'data': data, 'colors': colors, 'ticketpendingCS': ticketpendingCS,   'assignees_list_json': assignees_list_json, }
    
    return render(request, 'home/index.html', context)





    
    
    
    

