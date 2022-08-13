from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . models import *
  
class Gear_itemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gear_item
        # fields = ["id", "name", "desc", "price", "qty", 'image_url']
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):

    # This gear_item serializer is for the GET route
    gear_item = Gear_itemSerializer(many=True, read_only=True)

    # This serializer is for POST and PUT routes. The gear_item id is passed to back end for these methods
    gear_item_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Gear_item.objects.all()
    )
    class Meta:
        model = Reservation
        fields = ("start_date", "end_date", "gear_item", "qty", "user", "gear_item_ids")
        fields = "__all__"


    def create(self, validated_data):
        gear_items = validated_data.pop("gear_item_ids", None)
        # print('GEAR ITEMS AFTER POP: ', gear_items)
        # validated_data["user"] = self.context["request"].user
        reservation = Reservation.objects.create(**validated_data)
        if gear_items:
            reservation.gear_item.set(gear_items)
            # print('RESERVATION GEAR ITEM: ',reservation.gear_item)

        return reservation 
    
    def update(self, reservation, validated_data):
        reservation.start_date = validated_data.get('start_date', reservation.start_date)
        reservation.end_date = validated_data.get('end_date', reservation.end_date)
        reservation.qty = validated_data.get('qty', reservation.qty)
        gear_items = validated_data.pop("gear_item_ids", None)
        # print('GEAR ITEMS AFTER POP: ', gear_items)
        reservation.gear_item.set(gear_items)
        # print('GEAR ITEMS: ', gear_items)
        # print('RESERVATION GEAR ITEM: ', reservation.gear_item)

        reservation.save()
        return reservation



class UserSerializer(serializers.ModelSerializer):
    reservations = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Reservation.objects.all()
    )
    comments = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )
    posts = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )
    class Meta:
        model = User
        fields = ['id', 'username', 'reservations', 'posts', 'comments']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')
    # topic = serializers.ReadOnlyField(source='topic.name')
    # comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True, default=None)

    class Meta:
        model = Post
        # fields = ['id', 'title', 'body', 'user', 'comments', 'topic']
        fields = ['id', 'title', 'body', 'user']

class CommentSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Comment
        fields = ['id', 'body', 'user', 'post']


# SERIALIZERS FOR AUTH

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
