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
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    # gear_item = serializers.PrimaryKeyRelatedField(
    #     many=True, 
    #     queryset=Gear_item.objects.all(),
    #     read_only=False
    #     ),

    gear_item = Gear_itemSerializer(many=True, read_only=True)

    gear_item_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Gear_item.objects.all()
    )
    # gear_item = serializers.RelatedField(many=True, read_only=True)
    class Meta:
        model = Reservation
        fields = ("start_date", "end_date", "gear_item", "qty", "user", "gear_item_ids")
        fields = "__all__"

    # def create(self, validated_data):
    #     gear_item_data = validated_data.pop('gear_item')
    #     print("GEAR ITEM DATA: ", gear_item_data)
    #     reservation = Reservation.objects.create(**validated_data)
    #     return reservation

    def create(self, validated_data):
        gear_items = validated_data.pop("gear_item_ids", None)
        # validated_data["user"] = self.context["request"].user
        reservation = Reservation.objects.create(**validated_data)
        if gear_items:
            reservation.gear_item.set(gear_items)

        return reservation 





class UserSerializer(serializers.ModelSerializer):
    reservations = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Reservation.objects.all()
    )
    class Meta:
        model = User
        fields = ['id', 'username', 'reservations']


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
