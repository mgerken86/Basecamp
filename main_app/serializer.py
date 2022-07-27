
from rest_framework import serializers
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
    # gear_item = serializers.RelatedField(many=True, read_only=True)
    class Meta:
        model = Reservation
        # fields = ("start_date", "end_date", "gear_item", "qty", "user")
        fields = "__all__"

    # def create(self, validated_data):
    #     gear_item_data = validated_data.pop('gear_item')
    #     reservation = Reservation.objects.create(**validated_data)
    #     return reservation