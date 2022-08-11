
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Gear_item(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    qty = models.IntegerField(default=0)
    desc = models.TextField(max_length=300)
    image_url = models.CharField(max_length=500, default='https://a-lodge.com/wp-content/uploads/A-Lodge_No_Location_Grey-1200x221.png')
    # image_url = models.ImageField(upload_to='post_images')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'gear_item_id': self.id})

    

class Reservation(models.Model):
    start_date = models.DateField(("Start Date"), default=date.today)
    end_date = models.DateField(("End Date"), default=date.today)
    gear_item = models.ManyToManyField(Gear_item, related_name='gear_items')
    qty = models.SmallIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # total_price = models.SmallIntegerField(default=0)
    # reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    def get_total_price(self):
        total_price = 0
        for gear in self.gear_item:
            total_price += gear.price * gear.quantity

    def get_absolute_url(self):
        return reverse('reservation_detail', kwargs={'reservation_id': self.id})


# class Message_Board(models.Model):
#     topics = models.ForeignKey(Topic, on_delete=models.CASCADE)

class Topic(models.Model):
    name = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']

class Comment(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']

