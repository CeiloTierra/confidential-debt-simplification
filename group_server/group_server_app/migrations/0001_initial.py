# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-02 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('key', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('signature_inviter', models.CharField(max_length=400)),
                ('signature_group', models.CharField(default='', max_length=400)),
                ('signature_invitee', models.CharField(default='', max_length=400)),
                ('secret_code', models.CharField(max_length=20)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group_server_app.Group')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('key', models.CharField(max_length=400, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('confirmed', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group_server_app.Group')),
            ],
        ),
        migrations.AddField(
            model_name='invitation',
            name='invitee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitee', to='group_server_app.User'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='inviter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inviter', to='group_server_app.User'),
        ),
    ]
