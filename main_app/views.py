from django.shortcuts import render, redirect
from .models import Gear_item, Reservation
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ReservationForm


class GearList(ListView):
    model = Gear_item
class ReservationsList(ListView):
    model = Reservation


class Gear_itemCreate(CreateView):
    model = Gear_item
    fields = ['name', 'price', 'qty', 'desc']

class ReservationCreate(CreateView):
    model = Reservation
    fields = ["start_date", "end_date", "gear_item", "qty"]


# class ReservationDetail(DetailView):
#     model = Reservation
    
#     def get_context_data(self, **kwargs):
#         context = super(ReservationDetail, self).get_context_data(**kwargs)
#         context['gear_items'] = Gear_item.objects.all()
#         return context


class Gear_itemUpdate(UpdateView):
    model = Gear_item
    fields = ['name', 'price', 'qty', 'desc']

class ReservationUpdate(UpdateView):
    model = Reservation
    fields = "__all__"

class Gear_itemDelete(DeleteView):
    model = Gear_item
    success_url = '/rentals/'

class ReservationDelete(DeleteView):
    model = Reservation
    success_url = '/reservations/'


def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def rentals_index(request):
    gear_items = Gear_item.objects.all()
    return render(request, 'rentals/index.html', {'gear_items': gear_items})

def gear_item_detail(request, gear_item_id):
    gear_item = Gear_item.objects.get(id=gear_item_id)
    return render(request, 'rentals/detail.html', {'gear_item': gear_item})

def reservation_detail(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    gear_items = Gear_item.objects.all()
    reservation_form = ReservationForm()
    return render(request, 'reservations/reservation_detail.html', {
        'reservation': reservation,
        'gear_items': gear_items,
        'reservation_form': reservation_form
    })


def add_gear(request, reservation_id, gear_item_id):
    Reservation.objects.get(id=reservation_id).gear_item.add(gear_item_id)
    return redirect('reservation_detail', reservation_id=reservation_id)

