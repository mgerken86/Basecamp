from django.contrib import admin

from main_app.models import Gear_item, Reservation, Post, Comment, Topic

admin.site.register(Gear_item)
admin.site.register(Reservation)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Comment)
