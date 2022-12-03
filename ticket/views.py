import io
import json
import os.path
from datetime import datetime

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.conf import settings

from .TicketFactory import TicketFactory
from .models import Ticket


with open('config.json', 'r') as file:
    config = json.load(file)


def __generateTicket(inTicket: Ticket) -> HttpResponse:
    templatePath = os.path.join(settings.BASE_DIR, 'static/front.jpeg')
    factory = TicketFactory(inTicket.name, inTicket.contact, inTicket.seats, inTicket.total, inTicket.refId, templatePath)
    factory.FontPath = 'static/Segoe-UI-Font/SEGOEUI.TTF'
    factory.AddrSeats = (1280, 300)
    factory.AddrSeatCount = (1475, 300)
    factory.AddrTicketID = (1325, 350)
    factory.AddrTicketQRCode = (1275, 105)
    factory.AddrBuyerName = (110, 250)
    buff = io.BytesIO()
    factory.generate().save(buff, 'jpeg')
    response = HttpResponse(buff.getvalue(), content_type='image/jpeg')
    return response


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
        tickets = Ticket.objects.all().order_by('name')
        context = {
            'tickets': tickets,
            'tabTitle': 'Reports'
        }
        return render(request, 'ticket/report.html', context=context)
    else:
        return HttpResponse('Un-authorized operation')


def find(request):
    if 'meta' in request.session:
        if request.method == 'GET':
            return render(request, 'ticket/findTicket.html', context={'tabTitle': 'Find Tickets'})
        else:
            ticketNum = int(request.POST['ticket'])
            tickets = Ticket.objects.filter(refId=ticketNum)
            context = {
                'tickets': tickets,
                'tabTitle': 'Reports'
            }
            return render(request, 'ticket/report.html', context=context)
    else:
        return HttpResponse('Un-authorized operation')


def show(request):
    if 'meta' in request.session:
        if request.method == 'GET':
            ticketName = request.GET['q']
            if ticketName is not None and len(ticketName) > 0:
                ticket = Ticket.objects.filter(url=ticketName).first()
                return __generateTicket(ticket)
            else:
                return HttpResponse('Invalid request')
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
            for ticket in target:
                # target = Ticket.objects.filter(seatRow=row).filter(seatNum=col).first()
                bookedCols = list(map(int, ticket.seatNum.split(',')))
                for _ in range(fromNum, to + 1):
                    if _ in bookedCols:
                        messages.error(request, f'Seat {row}{_} is already booked')
                        return redirect(to='home')
        if ticketCount == 1:
            seats = f'{row}{fromNum}'
        else:
            seats = f'{row}{fromNum} - {row}{to}'
        try:
            newTicket = Ticket()
            newTicket.name = name
            newTicket.contact = contact
            newTicket.refId = int(datetime.now().timestamp())
            newTicket.total = ticketCount
            newTicket.seatRow = row
            newTicket.seatNum = ','.join([str(_) for _ in range(fromNum, to + 1)])
            newTicket.url = f'{name}_{newTicket.refId}.jpg'
            newTicket.seats = seats
            newTicket.save()
            return __generateTicket(newTicket)
        except Exception as e:
            targets = Ticket.objects.filter(seatRow=row)
            if len(targets) > 0:
                for seat in range(fromNum, to + 1):
                    target = Ticket.objects.filter(seatRow=row).filter(seatNum=seat).first()
                    if target is not None:
                        target.delete()
            messages.error(request, 'Failed to generate ticket. Report issue')
            print(e)
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
