# Generated by Django 4.1.3 on 2022-11-29 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_ticket_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='seats',
            field=models.TextField(default=''),
        ),
    ]
