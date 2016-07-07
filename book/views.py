import string
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ReservationForm
from .models import Reservation


class Error:
    def __init__(self, text):
        self.text = text
        self.flag = False
        
error = Error("")

def index(request):
    
    if request.method == "POST":
        
        form = ReservationForm(request.POST)
        
        if form.is_valid():
            # check and create reservation
            
            # create unsaved reservation from form
            reservation = form.save(commit=False)
            
            # check conditions
            text = "bla"
            error_flag = False
            if len(reservation.name.split()) < 2:
                error.text = "Indicar nombre y apellidos"
                error.flag = True
            if set(reservation.email) <= set(string.ascii_letters + string.digits + "!#$%&'*+-/=?^_`{|}~"):
                error.text = "Caracteres inválidos en el correo electrónico"
                error.flag = True
            if set(reservation.phone) <= set(string.digits + "+ "):
                error.text = "Caracteres inválidos en el número de teléfono"
                error.flag = True
            if reservation.initial_date >= reservation.final_date or reservation.initial_date < timezone.now().date():
                error.text = "Rango de fechas inválido"
                error.flag = True
            # not admitting check-out and check-in on the same day 
            # if len(Reservation.object.filter(initial_date__lte=reservation.final_date, final_date__gte=reservation.initial_date)) > 0:                
            if len(Reservation.objects.filter(initial_date__lt=reservation.final_date, final_date__gt=reservation.initial_date)) > 0:
                error.text = "Casa Dori no está disponible en ese rango de fechas"
                error.flag = True
                
            # redirect accordingly and reset the flag
            if error.flag:
                error.flag = False
                return redirect('rejection')
                 
                                
            else:
                # add pending info and save
                reservation.reservation_date = timezone.now()
                reservation.reference = get_random_string(length=8)
                reservation.save()
                
                # email
                subject = 'Reserva en Casa Dori'
                message = """
                Estimado/a {0}:
                
                
                Gracias por solicitar la reserva de Casa Dori entre el {1} y el {2}.
                
                El localizador de la reserva es {3}
                
                En breve, nos pondremos en contacto con usted para confirmar la reserva.
                
                
                Un saludo.
                
                Casa Dori
                """.format(reservation.name, reservation.initial_date.strftime('%d/%m/%Y'), reservation.final_date.strftime('%d/%m/%Y'), reservation.reference)
                from_email = settings.EMAIL_HOST_USER
                to_list = [reservation.email]
                send_mail(subject, message, from_email, to_list, fail_silently = True)
                
                return redirect('confirmation', pk=reservation.pk)
        
    else:
        
        form = ReservationForm()
    
    return render(request, 'book/index.html', {'form' : form})


def pics(request):
    return render(request, 'book/pics.html', {})

def confirmation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'book/confirmation.html', {'reservation' : reservation})
    
def rejection(request):
    return render(request, 'book/rejection.html', {'error' : error})

@staff_member_required
def housekeeping(request):
    successful = ""
    reservations = Reservation.objects.all()
    
    # clean
    if(request.GET.get('clean_button')):
        for res in reservations:
            if res.final_date < timezone.now().date():
                
                # send email
                subject = "[ANTIGUAS] Reserva del {0} al {1}".format(res.initial_date.strftime('%d/%m/%Y'), res.final_date.strftime('%d/%m/%Y'))
                message = """
                Nombre: {0}
                D.N.I.: {1}
                Correo electrónico: {2}
                Teléfono: {3}
                Fecha de entrada: {4}
                Fecha de salida: {5}
                Localizador: {6}
                Fecha de reserva: {7}
                Fecha de confirmación: {8}
                Fianza pagada: {9}
                Factura final pagada: {10}
                """.format(res.name,
                           res.dni,
                           res.email,
                           res.phone,
                           res.initial_date.strftime('%d/%m/%Y'),
                           res.final_date.strftime('%d/%m/%Y'),
                           res.reference,
                           res.reservation_date,
                           res.confirmation_date,
                           res.deposit,
                           res.invoice)
                from_email = settings.EMAIL_HOST_USER
                to_list = [settings.EMAIL_HOST_USER]
                send_mail(subject, message, from_email, to_list, fail_silently = True)
                
                # delete
                res.delete()
                
        successful = "Completado con éxito"
        
    # confirm
    if(request.GET.get('confirm')):
        # save in db
        pk = int(request.GET.get('pk'))
        reservation = get_object_or_404(Reservation, pk=pk)
        reservation.confirmation_date = timezone.now()
        reservation.save()
        
        # email
        subject = 'Reserva en Casa Dori'
        message = """
        Estimado/a {0}:
        
        
        Su reserva en Casa Dori entre el {1} y el {2} ha sido confirmada.
        
        El localizador de la reserva es {3}
        
        
        Un saludo.
        
        Casa Dori
        """.format(reservation.name, reservation.initial_date.strftime('%d/%m/%Y'), reservation.final_date.strftime('%d/%m/%Y'), reservation.reference)
        from_email = settings.EMAIL_HOST_USER
        to_list = [reservation.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
    # deposit
    if(request.GET.get('deposit')):
        pk = int(request.GET.get('pk'))
        reservation = get_object_or_404(Reservation, pk=pk)
        reservation.deposit = True
        reservation.save()
    
    # invoice
    if(request.GET.get('invoice')):
        pk = int(request.GET.get('pk'))
        reservation = get_object_or_404(Reservation, pk=pk)
        reservation.invoice = True
        reservation.save()
    
    # render
    return render(request, 'book/housekeeping.html', {'successful' : successful,
                                                      'reservations' : reservations})





## BUTTONS
# def f1(text):
#     return "a" + text
# 
# def myview(request):
#     message = "hola"
#     if(request.GET.get('mybtn')):
#         message = f1(text=request.GET.get('mytextbox'))
#     return render(request, 'myhtml.html', {'message' : message})
# 
# #     In book/housekeeping.html:
# #     <form action="#" method="get">
# #          <input type="text" value="8" name="mytextbox" size="1">
# #          <input type="submit" class="btn" value="Limpiar" name="mybtn">
# #     </form>
# #     {{ message }}
