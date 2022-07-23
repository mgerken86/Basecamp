from django.shortcuts import render
from .models import Gear_item


def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def rentals_index(request):
    gear_items = Gear_item.objects.all()
    return render(request, 'rentals/index.html', {'gear_items': gear_items})