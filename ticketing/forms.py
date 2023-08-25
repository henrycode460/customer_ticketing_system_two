from django import forms
from .models import Ticket
# from django_select2 import forms as s2forms
from apps.authentication.models import User
from django.utils import timezone
from ckeditor.widgets import CKEditorWidget
from django_select2.forms import Select2Widget

import json





        
class NewTicketForm(forms.ModelForm):
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assignee'].queryset = self.get_assignee_queryset()

    def get_assignee_queryset(self):
        # Filter technicians who don't have tickets with status 'Pending' or 'In_Progress'
        technicians = User.objects.filter(is_technician=True).exclude(ticket__status__in=['Pending', 'In_Progress']).distinct()

        return technicians
      
    class Meta:
        model = Ticket
        fields = ['customer', 'title', 'description', 'assignee']
        widgets = {
            'customer': Select2Widget,
            'title': forms.Select(choices=Ticket.Title, attrs={'class': 'form-control'}),
            'description': forms.CharField(widget=CKEditorWidget()),
            'assignee': Select2Widget,
        }

        
        
        
class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['customer', 'title', 'description', 'assignee', 'ticket_number']
        widgets = {
            'customer': Select2Widget,
            'title': forms.Select(choices=Ticket.Title, attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
             'assignee': Select2Widget,
        }






class TechnicianFeedbackForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ['technician_remark', 'attachments']
        



class ConversationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['conversation']
        widgets = {
            'conversation': forms.CharField(widget=CKEditorWidget()),
        }


    
class customerRejectionForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['customer_remark', 'customer_attachments']
        widgets = {
            
            'customer_remark': forms.Textarea(attrs={'class': 'form-control'}),
            
            
        }




    class UserProfileForm(forms.ModelForm):
     class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'address']
        widgets = {
            'is_admin': forms.Select(attrs={'class': 'form-control'}),
            'is_technician': forms.Select(attrs={'class': 'form-control'}),
            'is_customer_care': forms.Select(attrs={'class': 'form-control'}),
            'is_employee': forms.Select(attrs={'class': 'form-control'}),
            'is_supervisor': forms.Select(attrs={'class': 'form-control'}),
        }