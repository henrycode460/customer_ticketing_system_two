from django.urls import path



from . import views

# app_name = 'ticketing'
  
urlpatterns = [
path('add_ticket/', views.add_ticket, name='add_ticket'),
path('accept_ticket/<int:pk>/', views.accept_ticket, name='accept_ticket'),
path('all_ticket_created/', views.all_ticket_created, name='all_ticket_created'),
# path('ticket_to_claim_cs/', views.ticket_to_claim_cs, name="ticket_to_claim_cs"),
# path('ticket_intergration_cs/', views.ticket_intergration_cs, name="ticket_intergration_cs"),
path('ticket_queue/', views.ticket_queue, name="ticket_queue"),
path('update_ticket/<int:pk>', views.update_ticket, name="update_ticket"),
# path('technicain_feedback/<int:pk>', views.technicain_feedback, name='technicain_feedback'),
path('ticket_details/<int:pk>/', views.ticket_details, name='ticket_details'),
# path('postpone_ticket/<int:pk>', views.postpone_ticket, name="postpone_ticket"),
path('complete_ticket_customer/<int:pk>/', views.complete_ticket_customer, name="complete_ticket_customer"),
path('close_ticket/<int:pk>', views.close_ticket, name="close_ticket"),
path('ticket_in_progress/', views.ticket_in_progress, name="ticket_in_progress"),
# path('all_ticket_created_tech/', views.all_ticket_created_tech, name='all_ticket_created_tech'),
path('ticket_to_claim_tech/', views.ticket_to_claim_tech, name='ticket_to_claim_tech'),
path('ticket_report/', views.ticket_report, name="ticket_report"),
# path('ticket_intergration/', views.ticket_intergration, name="ticket_intergration"),
path('customer_approve/<int:pk>/', views.customer_approve, name="customer_approve"),
path('complete_ticket/<int:pk>/', views.complete_ticket, name="complete_ticket"),
# # path('delete_ticket/<int:pk>/', views.delete_ticket, name="delete_ticket"),
path('ticket_completed/', views.ticket_completed, name="ticket_completed"),
# path('export_csv_filter/', views.export_csv_filter, name="export_csv_filter"),
# path('export_pdf_filter/', views.export_pdf_filter, name="export_pdf_filter"),
 path('download/<path:attachment_url>/', views.download_attachment, name='download_attachment'),
 path('technician_complete_ticket/', views.technician_complete_ticket, name="technician_complete_ticket"),
 path('reject_ticket_form/<int:pk>/', views.reject_ticket_form, name='reject_ticket_form'),
 path('user_activity_log/', views.user_activity_log, name="user_activity_log"),
path('technician_complete_ticket_admin/', views.technician_complete_ticket_admin, name="technician_complete_ticket_admin"),
path('user_activities/', views.user_activities_view, name='user_activities'),
path('customer_queue/', views.customer_queue, name='customer_queue'),


path('send_email/', views.send_email, name='send_email'),

path('api/create_ticket/', views.create_ticket_api, name='create_ticket_api'),






    
 ]