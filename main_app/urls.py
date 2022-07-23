from django.urls import path
from . import views
from main_app.views import GearList

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('rentals/', views.rentals_index, name='index'),
    # path('rentals/', GearList.as_view(), name='index'),
    path('rentals/<int:gear_item_id>', views.gear_item_detail, name='detail'),
    path('rentals/create', views.Gear_itemCreate.as_view(), name='gear_item_create'),
    path('rentals/<int:pk>/update', views.Gear_itemUpdate.as_view(), name='gear_item_update'),
    path('rentals/<int:pk>/delete', views.Gear_itemDelete.as_view(), name='gear_item_delete'),
]