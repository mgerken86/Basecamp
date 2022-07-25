
from rest_framework import serializers
from . models import *
  
class Gear_itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gear_item
        fields = "__all__"