# Generated by Django 4.1.3 on 2022-11-29 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_ticket_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='refId',
            field=models.PositiveBigIntegerField(),
        ),
    ]