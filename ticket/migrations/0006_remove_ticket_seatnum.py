# Generated by Django 4.1.3 on 2022-12-03 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0005_alter_ticket_refid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='seatNum',
        ),
    ]
