# Generated by Django 4.1.3 on 2022-12-03 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_remove_ticket_seatnum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='contact',
            field=models.PositiveBigIntegerField(max_length=10),
        ),
    ]
