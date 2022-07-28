from functools import partial
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Gear_item, Reservation, Photo
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .forms import ReservationForm
import requests
import json
import boto3
import os
import uuid
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . serializer import *
from main_app import serializer
# Create your views here.


# API FETCH FOR WEATHER DATA ->
# def fetchApi(list):

#     url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

#     querystring = {"q":"Boulder","days":"3"}

#     headers = {
#         "X-RapidAPI-Key": "b706fa8596msha33725def79a97cp1b9fc1jsn8dfd397c7442",
#         "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
#     }

#     response = requests.request("GET", url, headers=headers, params=querystring)

#     data = response.text
#     parse_jason = json.loads(data)
#     forecast = parse_jason['forecast']['forecastday']

#     for day in forecast:
#         list.append(day)

  
class Gear_itemList(APIView):
    
    serializer_class = Gear_itemSerializer
  
    def get(self, request):
        detail = [ {
            "id": detail.id,
            "name": detail.name,
            "desc": detail.desc,
            "price": detail.price,
            "qty": detail.qty
            } 
        for detail in Gear_item.objects.all()]
        return Response(detail)
  
    def post(self, request):
        serializer = Gear_itemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return  Response(serializer.data)


class Gear_itemDetail(APIView):
    def get_object(self, gear_item_id, format=None):
        return Gear_item.objects.get(id=gear_item_id)
    
    def get(self, request, gear_item_id, format=None):
        gear_item = self.get_object(gear_item_id)
        serializer = Gear_itemSerializer(gear_item)
        return Response(serializer.data)

    def put(self, request, gear_item_id, format=None):
        gear_item = self.get_object(gear_item_id)
        serializer = Gear_itemSerializer(gear_item, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response('gear item was updated')

    def delete(self, request, gear_item_id, format=None):
        gear_item = self.get_object(gear_item_id)
        gear_item.delete()
        return Response('gear item is deleted')


class ReservationIndex(APIView):
    
    serializer_class = ReservationSerializer

    def get(self, request, format=None):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
  
    def post(self, request):
        # gear_item = request.data['gear_item']
        # print(gear_item)
        # request.data['gear_item'] = Gear_item.objects.get(id = gear_item)
        # print(request.data['gear_item'])
        serializer = ReservationSerializer(data=request.data, partial=True)
        print(serializer)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return  Response(serializer.data)

class Reservation_itemDetail(APIView):
    def get_object(self, reservation_id, format=None):
        return Reservation.objects.get(id=reservation_id)

    def get(self, request, reservation_id, format=None):
        print('IN THE VIEW')
        reservation = self.get_object(reservation_id)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)


    def put(self, request, reservation_id, format=None):
        reservation = self.get_object(reservation_id)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response('gear item was updated')

    def delete(self, request, reservation_id, format=None):
        print("THIS IS THE DELETE ID", reservation_id)
        reservation = self.get_object(reservation_id)
        print("THIS IS THE RESERVATION", reservation)
        reservation.delete()
        return Response('gear item is deleted')



# class GearList(ListView):
#     model = Gear_item
class ReservationsList(ListView):
    model = Reservation


class Gear_itemCreate(CreateView):
    model = Gear_item
    fields = ['name', 'price', 'qty', 'desc']



class ReservationCreate(CreateView):
    model = Reservation
    fields = ["start_date", "end_date", "gear_item", "qty"]

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)




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
    forecast_list = []
    fetchApi(forecast_list)
    gear_items = Gear_item.objects.all()
    return render(request, 'rentals/index.html', {
        'gear_items': gear_items,
        'forecast_list': forecast_list
        })

def gear_item_detail(request, gear_item_id):
    gear_item = Gear_item.objects.get(id=gear_item_id)
    return render(request, 'rentals/detail.html', {'gear_item': gear_item})

def reservation_detail(request, reservation_id):
    # reservation = Reservation.objects.get(user=request.user)
    reservation = Reservation.objects.get(id=reservation_id)
    gear_items = Gear_item.objects.all()
    reservation_form = ReservationForm()
    context = {
        'reservation': reservation,
        'gear_items': gear_items,
        'reservation_form': reservation_form,
    }
    return render(request, 'reservations/reservation_detail.html', context)


def add_gear(request, reservation_id, gear_item_id):
    this_reservation = Reservation.objects.get(id=reservation_id)
    this_reservation.gear_item.add(gear_item_id)
    return redirect('reservation_detail', reservation_id=reservation_id)

def remove_gear(request, reservation_id, gear_item_id):
    this_reservation = Reservation.objects.get(id=reservation_id)
    this_reservation.gear_item.remove(gear_item_id)
    return redirect('reservation_detail', reservation_id=reservation_id)

def add_quantity(request, reservation_id):
    this_reservation = Reservation.objects.get(id=reservation_id)
    this_reservation.qty += 1
    this_reservation.save()
    return redirect('reservation_detail', reservation_id=reservation_id)

def remove_quantity(request, reservation_id):
    this_reservation = Reservation.objects.get(id=reservation_id)
    this_reservation.qty -= 1
    this_reservation.save()
    return redirect('reservation_detail', reservation_id=reservation_id)


def add_photo(request, gear_item_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, gear_item_id=gear_item_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', gear_item_id=gear_item_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


# AUTH VIEWS 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET', "POST"])
def getRoutes(request):
    routes = [
        'token/',
        'register/',
        'token/refresh/'
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)

