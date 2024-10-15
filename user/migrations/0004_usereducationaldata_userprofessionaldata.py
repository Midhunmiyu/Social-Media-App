# Generated by Django 5.1.2 on 2024-10-15 06:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_profile_dob_remove_profile_gender_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEducationalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(blank=True, max_length=255, null=True)),
                ('school', models.CharField(blank=True, max_length=255, null=True)),
                ('university', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('still_studying', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_educational_data', to='user.profile')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfessionalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.CharField(blank=True, max_length=155, null=True)),
                ('company', models.CharField(blank=True, max_length=155, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('still_working', models.BooleanField(default=False)),
                ('self_employed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_professional_data', to='user.profile')),
            ],
        ),
    ]