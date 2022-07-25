from django.urls import path
from . import views
from main_app.views import ReservationsList

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('rentals/', views.rentals_index, name='index'),
    path('rentals/<int:gear_item_id>', views.gear_item_detail, name='detail'),
    path('rentals/create', views.Gear_itemCreate.as_view(), name='gear_item_create'),
    path('rentals/<int:pk>/update', views.Gear_itemUpdate.as_view(), name='gear_item_update'),
    path('rentals/<int:pk>/delete', views.Gear_itemDelete.as_view(), name='gear_item_delete'),
    path('rentals/<int:gear_item_id>/add_photo/', views.add_photo, name='add_photo'),
    path('reservations/', ReservationsList.as_view(), name='reservations_index'),
    path('reservations/new', views.ReservationCreate.as_view(), name='reservation_create'),
    path('reservations/<int:reservation_id>', views.reservation_detail, name='reservation_detail'),
    path('reservations/<int:pk>/update', views.ReservationUpdate.as_view(), name='reservation_update'),
    path('reservations/<int:reservation_id>/add_gear/<int:gear_item_id>', views.add_gear, name='add_gear'),
    path('reservations/<int:reservation_id>/remove_gear/<int:gear_item_id>', views.remove_gear, name='remove_gear'),
    path('reservations/<int:reservation_id>/add_quantity/', views.add_quantity, name='add_quantity'),
    path('reservations/<int:reservation_id>/remove_quantity/', views.remove_quantity, name='remove_quantity'),
    path('reservations/<int:pk>/delete', views.ReservationDelete.as_view(), name='reservation_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]