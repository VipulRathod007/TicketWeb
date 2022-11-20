from django.db import models


class Ticket(models.Model):
    refId = models.IntegerField()
    name = models.TextField()
    contact = models.IntegerField(max_length=10)
    seatRow = models.CharField(max_length=1)
    seatNum = models.IntegerField()
    url = models.TextField(default='')

    def __str__(self):
        return f'{self.name} - {self.seatRow}:{self.seatNum}'
