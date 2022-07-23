from django.shortcuts import render
from .models import Gear_item, Reservation
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class GearList(ListView):
    model = Gear_item
class ReservationsList(ListView):
    model = Reservation


class Gear_itemCreate(CreateView):
    model = Gear_item
    fields = ['name', 'price', 'qty', 'desc']

class ReservationCreate(CreateView):
    model = Reservation
    fields = "__all__"
    success_url = '/reservations'

class ReservationDetail(DetailView):
    model = Reservation

class Gear_itemUpdate(UpdateView):
    model = Gear_item
    fields = ['name', 'price', 'qty', 'desc']

class Gear_itemDelete(DeleteView):
    model = Gear_item
    success_url = '/rentals/'


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