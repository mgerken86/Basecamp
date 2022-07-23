from django.shortcuts import render
from .models import Gear_item
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class GearList(ListView):
    model = Gear_item
    # template_name = 'rentals/index.html'

class Gear_itemCreate(CreateView):
    model = Gear_item
    fields = ['name', 'price', 'qty', 'desc']

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
    return render(request, 'rentals/index.html', {'gear_items': gear_items})

def gear_item_detail(request, gear_item_id):
    gear_item = Gear_item.objects.get(id=gear_item_id)
    return render(request, 'rentals/detail.html', {'gear_item': gear_item})