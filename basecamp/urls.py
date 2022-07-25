
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('rentals', include('main_app.urls')),
    # path('events',  include('main_app.urls')),
    # path('messageboard',  include('main_app.urls'))
]
