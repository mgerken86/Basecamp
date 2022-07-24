from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Gear_item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    qty = models.IntegerField()
    desc = models.TextField(max_length=300)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'gear_item_id': self.id})
    

# class Reservation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     total = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)

# class Reservation_item(models.Model):
#     start_date = models.DateField(("Start Date"), default=date.today),
#     end_date = models.DateField(("Return Date"), default=date.today),
#     gear_item = models.ManyToManyField(Gear_item),
#     reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

class Reservation(models.Model):
    start_date = models.DateField(("Start Date"), default=date.today)
    end_date = models.DateField(("Return Date"), default=date.today)
    gear_item = models.OneToOneField(Gear_item, on_delete=models.CASCADE)
    qty = models.SmallIntegerField(default=1)
    # reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    def total_price(self):
        return self.qty * self.gear_item.price

    def get_absolute_url(self):
        return reverse('reservation_detail', kwargs={'reservation_id': self.id})
