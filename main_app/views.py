from functools import partial
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login
from .models import Gear_item, Reservation, Topic, Post, Comment
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
import requests
import json
import boto3
import os
import uuid
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from . serializer import *



class Gear_itemList(APIView):
    serializer_class = Gear_itemSerializer
    # parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        detail = [{
            "id": detail.id,
            "name": detail.name,
            "desc": detail.desc,
            "price": detail.price,
            "qty": detail.qty,
            "image_url": detail.image_url
        }
            for detail in Gear_item.objects.all()]
        return Response(detail)

    def post(self, request):
        serializer = Gear_itemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class Gear_itemDetail(APIView):
    # parser_classes = (MultiPartParser, FormParser)

    def get_object(self, gear_item_id, format=None):
        return Gear_item.objects.get(id=gear_item_id)

    def get(self, request, gear_item_id, format=None):
        gear_item = self.get_object(gear_item_id)
        serializer = Gear_itemSerializer(gear_item)
        return Response(serializer.data)

    def put(self, request, gear_item_id, format=None):
        gear_item = self.get_object(gear_item_id)
        print(gear_item)
        serializer = Gear_itemSerializer(
            gear_item, data=request.data, partial=True)
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
        serializer = ReservationSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class Reservation_itemDetail(APIView):
    def get_object(self, reservation_id, format=None):
        return Reservation.objects.get(id=reservation_id)

    def get(self, request, reservation_id, format=None):
        reservation = self.get_object(reservation_id)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    def put(self, request, reservation_id, format=None):
        reservation = self.get_object(reservation_id)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response('reservation was updated')

    def delete(self, request, reservation_id, format=None):
        reservation = self.get_object(reservation_id)
        reservation.delete()
        return Response('reservation is deleted')


class UserReservationIndex(APIView):
    serializer_class = UserSerializer

    def get(self, request, user_id, format=None):
        reservations = Reservation.objects.filter(user=user_id)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

class TopicList(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        serializer.save()


class PostIndex(APIView):
    serializer_class = PostSerializer

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)


class Post_Detail(APIView):
    def get_object(self, post_id, format=None, partial=True):
        return Post.objects.get(id=post_id)

    def get(self, request, post_id, format=None):
        post = self.get_object(post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_id, format=None):
        post = self.get_object(post_id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response('post is updated')

    def delete(self, request, post_id, format=None):
        post = self.get_object(post_id)
        post.delete()
        return Response('post is deleted')

class CommentIndex(APIView):
    serializer_class = CommentSerializer

    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class CommentDetail(APIView):
    def get_object(self, comment_id, format=None):
        return Comment.objects.get(id=comment_id)

    def get(self, request, comment_id, format=None):
        print('IN THE VIEW')
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    # def put(self, request, reservation_id, format=None):
    #     print("SELF: ", self)
    #     reservation = self.get_object(reservation_id)
    #     serializer = ReservationSerializer(reservation, data=request.data)
    #     print(request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response('reservation was updated')

    # def delete(self, request, reservation_id, format=None):
    #     print("THIS IS THE DELETE ID", reservation_id)
    #     reservation = self.get_object(reservation_id)
    #     print("THIS IS THE RESERVATION", reservation)
    #     reservation.delete()
    #     return Response('gear item is deleted')


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
