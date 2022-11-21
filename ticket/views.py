import json
import os.path

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.conf import settings

from .TicketFactory import TicketFactory
from .models import Ticket


with open('config.json', 'r') as file:
    config = json.load(file)


def home(request):
    if request.method == 'GET':
        if 'meta' in request.session:
            context = {
                'rows': config['rows'],
                'tabTitle': 'Books tickets'
            }
            return render(request, 'ticket/index.html', context=context)
        else:
            return redirect(to='login')
    else:
        messages.error(request, 'Method not allowed')
        return redirect(to='home')


def report(request):
    if 'meta' in request.session:
        tickets = Ticket.objects.values('name', 'contact', 'refId', 'url').annotate(tickets=Count('refId')).order_by()
        context = {
            'tickets': tickets,
            'tabTitle': 'Reports'
        }
        return render(request, 'ticket/report.html', context=context)
    else:
        return HttpResponse('Un-authorized operation')


def book(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact = int(request.POST['contact'])
        row = request.POST['row']
        fromNum = int(request.POST['from'])
        to = int(request.POST['to'])
        ticketCount = to - fromNum + 1
        if len(str(contact)) != 10:
            messages.error(request, 'Invalid Contact number')
            return redirect(to='home')
        elif ticketCount <= 0:
            messages.error(request, 'Starting no. must be less than or equal to Ending no.')
            return redirect(to='home')
        elif row not in config['rows'] or config['rows'][row] < to or fromNum <= 0:
            messages.error(request, f'Selected seat {row}{fromNum} - {row}{to} is Invalid')
            return redirect(to='home')
        target = Ticket.objects.filter(seatRow=row)
        if len(target) > 0:
            for col in range(fromNum, to + 1):
                target = Ticket.objects.filter(seatRow=row).filter(seatNum=col).first()
                if target is not None:
                    messages.error(request, f'Seat {row}{col} is already booked')
                    return redirect(to='home')
        if ticketCount == 1:
            seats = f'{row}{fromNum}'
        else:
            seats = f'{row}{fromNum} - {row}{to}'
        templatePath = os.path.join(settings.BASE_DIR, 'assets/front.png')
        ticketsPath = os.path.join(settings.BASE_DIR, 'assets/Tickets')
        factory = TicketFactory(name, contact, seats, ticketCount, templatePath)
        newTicketPath = os.path.join(settings.STATIC_ROOT, f'{name}_{factory.Ticket.ID}.pdf')
        factory.AddrSeats = (1600, 380)
        factory.AddrSeatCount = (1850, 380)
        factory.AddrTicketID = (1675, 445)
        factory.AddrTicketQRCode = (1590, 85)
        factory.AddrBuyerName = (110, 325)
        try:
            for seat in range(fromNum, to + 1):
                newTicket = Ticket()
                newTicket.name = name
                newTicket.contact = contact
                newTicket.refId = factory.Ticket.ID
                newTicket.seatRow = row
                newTicket.seatNum = seat
                newTicket.url = newTicketPath
                newTicket.save()
            factory.generate().save(newTicketPath)
            messages.success(request, 'Ticket booked successfully!')
            return redirect(to='home')
        except Exception:
            targets = Ticket.objects.filter(seatRow=row)
            if len(target) > 0:
                for seat in range(fromNum, to + 1):
                    target = Ticket.objects.filter(seatRow=row).filter(seatNum=seat).first()
                    if target is not None:
                        target.delete()
            messages.error(request, 'Failed to generate ticket. Report issue')
            return redirect(to='home')
    else:
        messages.error(request, 'Method not allowed')
        return redirect(to='home')


def login(request):
    if request.method == 'GET':
        if 'meta' in request.session:
            return redirect(to='home')
        context = {
            'tabTitle': 'Login'
        }
        return render(request, 'ticket/login.html', context=context)
    else:
        uid = request.POST['uid']
        pwd = request.POST['pwd']
        if uid == 'khadkhdat' and pwd == 'Comedy@18Dec':
            request.session['meta'] = True
            return redirect(to='home')
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect(to='login')


def logout(request):
    request.session.pop('meta')
    return redirect(to='home')
