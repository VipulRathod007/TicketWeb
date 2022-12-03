from django.db import models


class Ticket(models.Model):
    refId = models.PositiveBigIntegerField()
    name = models.TextField()
    contact = models.PositiveBigIntegerField(max_length=10)
    seatRow = models.CharField(max_length=1)
    seatNum = models.TextField(default='')
    url = models.TextField(default='')
    seats = models.TextField(default='')
    total = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.name} - {self.seatRow}:{self.seatNum}'
