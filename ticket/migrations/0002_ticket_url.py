# Generated by Django 4.1.3 on 2022-11-20 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='url',
            field=models.TextField(default=''),
        ),
    ]