
from rest_framework import serializers
from . models import *
  
class Gear_itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gear_item
        fields = "__all__"
    
    def create(self, validated_data):
        return Gear_item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.price = validated_data.get('price', instance.price)
        instance.qty = validated_data.get('qty', instance.qty)

        instance.save()
        return instance

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"