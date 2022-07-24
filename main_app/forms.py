from django.forms import ModelForm
from .models import Reservation

class ReservationForm(ModelForm):
  class Meta:
    model = Reservation
    fields = ['start_date', 'end_date', 'gear_item', 'qty']
