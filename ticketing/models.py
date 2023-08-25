from django.db import models
import random

from django.utils import timezone

import json
# # Create your models here.

from django.db import models
# from django.contrib.auth.models import User
from apps.authentication.models import User
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
import uuid

import re

from django.conf import settings
# from django_user_agents.utils import get_user_agent

import requests


# # Create your models here.

 

# #customer
class Customer(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=100, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    service = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    enabled = models.CharField(max_length=100, null=True, blank=True)
    active = models.CharField(max_length=100, null=True, blank=True)
  
    technology = models.CharField(max_length=100, null=True, blank=True)
    customer_type = models.CharField(max_length=100, null=True, blank=True)
   
   
    
    
    def __str__(self):
        return self.name
    
 

# # Ticket class

class Ticket(models.Model):
    
    
    TicketStatus = (
        ('Pending', 'Pending'),
        ('In_Progress', 'In Progress'),
	    ('Completed', 'Completed'),
	    ('Cancel', 'Cancel'),
        ('Postpone', 'Postpone'),
        ('TechComplete', 'TechComplete'),
        ('CustomerApproved', 'CustomerApproved'),
        ('CustomerDisproved', 'CustomerDisproved'),		
	)
    
    Title= ( 
        ('New Installation', 'New Installation'),
        ('Support', 'Support'),
	    ('Re-Connection', 'Re-Connection'),
        ('Retriver', 'Retriver'),
        ('New Assessment', 'New Assessment'),
	    	
	)
    
    
    ticket_number = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, choices=Title, default='Support')
    description = RichTextField(blank=True, null=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    status = models.CharField(max_length=50, choices=TicketStatus, default='Pending')
    date_created = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True )
    is_resolve = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_tickets')
    close_date = models.DateTimeField(null=True, blank=True)
    cancel_date = models.DateTimeField(null=True, blank=True)
    rejected_date = models.DateTimeField(null=True, blank=True)
    postpone_date = models.DateTimeField(null=True, blank=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    customer_approve_date = models.DateTimeField(null=True, blank=True)
    technician_remark = models.TextField(max_length=300, null=True, blank=True)
    customer_remark = models.TextField(max_length=300, null=True, blank=True)
    customer_attachments = models.FileField(upload_to='attachments/', blank=True, null=True)
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)
   

   
    conversation = RichTextField(blank=True, null=True)
    conversation_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
           
            existing_ticket_numbers = Ticket.objects.values_list('ticket_number', flat=True)
            new_ticket_number = None

            while not new_ticket_number or new_ticket_number in existing_ticket_numbers:
                new_ticket_number = random.randint(10000, 99999)

            self.ticket_number = new_ticket_number

        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return self.title
    

class MessageReadStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'ticket')
    


# class UserActivity(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     activity = models.CharField(max_length=100)
#     details = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         if self.user:
#             return f"{self.user.username} - {self.activity} - {self.timestamp}"
#         else:
#             return f"Unknown User - {self.activity} - {self.timestamp}"

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    user_agent = models.CharField(max_length=255, blank=True, null=True)

    ip_address = models.GenericIPAddressField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    
    region = models.CharField(max_length=255, blank=True, null=True)
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

  

  
    

   