# Generated by Django 3.2.6 on 2023-08-06 02:04

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('zip', models.CharField(blank=True, max_length=100, null=True)),
                ('place', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('service', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('enabled', models.CharField(blank=True, max_length=100, null=True)),
                ('active', models.CharField(blank=True, max_length=100, null=True)),
                ('technology', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_type', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=255)),
                ('details', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_agent_string', models.TextField(blank=True, null=True)),
                ('device_info', models.CharField(blank=True, max_length=255, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_number', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(choices=[('New Installation', 'New Installation'), ('Support', 'Support'), ('Re-Connection', 'Re-Connection'), ('Retriver', 'Retriver'), ('New Assessment', 'New Assessment')], default='Support', max_length=50)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('In_Progress', 'In Progress'), ('Completed', 'Completed'), ('Cancel', 'Cancel'), ('Postpone', 'Postpone'), ('TechComplete', 'TechComplete'), ('CustomerApproved', 'CustomerApproved'), ('CustomerDisproved', 'CustomerDisproved')], default='Pending', max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_resolve', models.BooleanField(default=False)),
                ('accepted_date', models.DateTimeField(blank=True, null=True)),
                ('close_date', models.DateTimeField(blank=True, null=True)),
                ('cancel_date', models.DateTimeField(blank=True, null=True)),
                ('rejected_date', models.DateTimeField(blank=True, null=True)),
                ('postpone_date', models.DateTimeField(blank=True, null=True)),
                ('customer_approve_date', models.DateTimeField(blank=True, null=True)),
                ('technician_remark', models.TextField(blank=True, max_length=300, null=True)),
                ('customer_remark', models.TextField(blank=True, max_length=300, null=True)),
                ('customer_attachments', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('attachments', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('conversation', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('conversation_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('accepted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accepted_tickets', to=settings.AUTH_USER_MODEL)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketing.customer')),
            ],
        ),
        migrations.CreateModel(
            name='MessageReadStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketing.ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'ticket')},
            },
        ),
    ]
