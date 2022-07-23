from django.db import models


class Gear_item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    qty = models.IntegerField()
    desc = models.TextField(max_length=300)

    def __str__(self):
        return self.name

# class Reservation_item(models.Model):
#     start_date = models.DateField(),
#     end_date = models.DateField(),
#     reservation = models.ForeignKey('Reservation', on_delete=models.SET_NULL, null=True, blank=True)
#     gear_item = models.ForeignKey('Gear_item', on_delete=models.SET_NULL, null=True, blank=True)

# class Reservation(models.Model):
#     user = models.ForeignKey(User)
#     total = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
