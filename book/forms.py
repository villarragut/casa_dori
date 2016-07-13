from django import forms
from django.utils import timezone
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('name', 'dni', 'email', 'phone', 'guests', 'initial_date', 'final_date',)
        widgets = {'initial_date' :  forms.DateInput(attrs={'class':'datepicker'}),
                   'final_date' :  forms.DateInput(attrs={'class':'datepicker'}),}
        #widgets = {'initial_date' :  forms.SelectDateWidget(years=range(timezone.now().year, timezone.now().year + 2)),
        #          'final_date' :  forms.DateInput(attrs={'class':'datepicker'}),}