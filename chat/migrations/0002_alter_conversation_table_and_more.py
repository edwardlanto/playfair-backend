# Generated by Django 4.2.1 on 2023-07-03 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='conversation',
            table='conversation',
        ),
        migrations.AlterModelTable(
            name='conversationmember',
            table='conversation_member',
        ),
        migrations.AlterModelTable(
            name='message',
            table='message',
        ),
    ]
