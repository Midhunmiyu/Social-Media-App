# Generated by Django 5.1.2 on 2024-10-22 11:54

import django.db.models.deletion
import userpost.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='PostMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_file', models.FileField(blank=True, null=True, upload_to=userpost.models.user_posts_directory_path)),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], max_length=5)),
                ('user_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_media', to='userpost.posts')),
            ],
        ),
    ]
