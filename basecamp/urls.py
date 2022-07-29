
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('rentals', include('main_app.urls')),
    # path('events',  include('main_app.urls')),
    # path('messageboard',  include('main_app.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
