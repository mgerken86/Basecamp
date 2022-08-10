from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from main_app.views import Gear_itemList, Gear_itemDetail, ReservationIndex, UserReservationIndex
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('rentals/', Gear_itemList.as_view()),
    path('rentals/<int:gear_item_id>', Gear_itemDetail.as_view()),
    path('reservations/', ReservationIndex.as_view()),
    path('reservations/<int:reservation_id>', views.Reservation_itemDetail.as_view(), name='reservation_detail'),
    path('myaccount/<int:user_id>', views.UserReservationIndex.as_view()),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('', views.getRoutes),
    path('test/', views.testEndPoint, name='test')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)